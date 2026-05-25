"""数据库迁移脚本：为 users 表添加 email 字段。

此脚本执行以下步骤：
1. 检查 email 列是否存在，不存在则添加（nullable=True）
2. 为现有用户填充默认邮箱地址
3. 将 email 列设为 NOT NULL

使用方式：
    cd backend && python -m scripts.migrate_add_email
"""

import asyncio
import sys
from pathlib import Path

# 将 backend 目录加入 Python 路径
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from app.core.config import settings


async def column_exists(engine, table_name: str, column_name: str) -> bool:
    """检查指定表的列是否存在。"""
    async with engine.connect() as conn:
        result = await conn.execute(
            text(
                "SELECT COUNT(*) FROM information_schema.COLUMNS "
                "WHERE TABLE_SCHEMA = DATABASE() "
                "AND TABLE_NAME = :table_name "
                "AND COLUMN_NAME = :column_name"
            ),
            {"table_name": table_name, "column_name": column_name},
        )
        return result.scalar() > 0


async def add_email_column(engine) -> None:
    """添加 email 列（nullable）。"""
    print("  添加 email 列（nullable=True）...")
    async with engine.begin() as conn:
        await conn.execute(
            text(
                "ALTER TABLE users "
                "ADD COLUMN email VARCHAR(255) NULL UNIQUE"
            )
        )
    print("  ✓ email 列已添加")


async def fill_default_emails(engine) -> None:
    """为现有用户填充默认邮箱地址。"""
    async with engine.connect() as conn:
        # 统计需要更新的用户数
        result = await conn.execute(
            text("SELECT COUNT(*) FROM users WHERE email IS NULL")
        )
        count = result.scalar()

        if count == 0:
            print("  所有用户已有邮箱，跳过填充")
            return

        print(f"  为 {count} 个用户填充默认邮箱...")

        # 为每个用户生成 username@placeholder.local 邮箱
        await conn.execute(
            text(
                "UPDATE users "
                "SET email = CONCAT(username, '@placeholder.local') "
                "WHERE email IS NULL"
            )
        )
        await conn.commit()

    print("  ✓ 默认邮箱已填充")


async def set_email_not_null(engine) -> None:
    """将 email 列设为 NOT NULL。"""
    print("  设置 email 列为 NOT NULL...")
    async with engine.begin() as conn:
        await conn.execute(
            text("ALTER TABLE users MODIFY COLUMN email VARCHAR(255) NOT NULL")
        )
    print("  ✓ email 列已设为 NOT NULL")


async def main() -> None:
    """执行迁移流程。"""
    print("=" * 50)
    print("数据库迁移：添加 email 字段到 users 表")
    print("=" * 50)
    print()

    engine = create_async_engine(
        settings.database_url,
        pool_pre_ping=False,  # aiomysql 不兼容 pool_pre_ping
        echo=False,
    )

    try:
        # 步骤 1：检查并添加列
        if await column_exists(engine, "users", "email"):
            print("步骤 1/3：email 列已存在，跳过添加")
        else:
            print("步骤 1/3：添加 email 列")
            await add_email_column(engine)
        print()

        # 步骤 2：填充默认值
        print("步骤 2/3：填充默认邮箱")
        await fill_default_emails(engine)
        print()

        # 步骤 3：设为 NOT NULL
        print("步骤 3/3：设置 NOT NULL 约束")
        await set_email_not_null(engine)
        print()

        print("=" * 50)
        print("迁移完成！")
        print("=" * 50)
        print()
        print("注意：默认填充的邮箱格式为 username@placeholder.local")
        print("建议通过用户中心让用户更新为真实邮箱地址。")

    except Exception as e:
        print(f"\n迁移失败：{e}")
        print("\n请检查数据库连接配置和权限。")
        raise
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
