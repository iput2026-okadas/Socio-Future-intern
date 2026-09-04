from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass(frozen=True)
class MySQLConfig:
    """MySQL接続設定。"""

    host: str
    port: int
    user: str
    password: str
    database: str
    batch_size: int = 1000


def load_mysql_config() -> MySQLConfig:
    """
    .envまたは環境変数からMySQL接続設定を読み込む。

    Raises:
        ValueError: 必須の環境変数が未設定、または数値設定が不正な場合。
    """
    load_dotenv()

    required_names = [
        "MYSQL_HOST",
        "MYSQL_USER",
        "MYSQL_PASSWORD",
        "MYSQL_DATABASE",
    ]

    missing_names = [
        name for name in required_names if os.getenv(name) is None
    ]

    if missing_names:
        missing_text = ", ".join(missing_names)
        raise ValueError(
            f"必須の環境変数が設定されていません: {missing_text}"
        )

    try:
        port = int(os.getenv("MYSQL_PORT", "3306"))
    except ValueError as exc:
        raise ValueError(
            "MYSQL_PORTには整数を指定してください。"
        ) from exc

    try:
        batch_size = int(os.getenv("MYSQL_BATCH_SIZE", "1000"))
    except ValueError as exc:
        raise ValueError(
            "MYSQL_BATCH_SIZEには整数を指定してください。"
        ) from exc

    if port <= 0:
        raise ValueError(
            "MYSQL_PORTには1以上の整数を指定してください。"
        )

    if batch_size <= 0:
        raise ValueError(
            "MYSQL_BATCH_SIZEには1以上の整数を指定してください。"
        )

    return MySQLConfig(
        host=os.environ["MYSQL_HOST"],
        port=port,
        user=os.environ["MYSQL_USER"],
        password=os.environ["MYSQL_PASSWORD"],
        database=os.environ["MYSQL_DATABASE"],
        batch_size=batch_size,
    )

@dataclass(frozen=True)
class AWSConfig:
    """AWS/S3接続設定。"""

    profile: str
    region: str
    bucket: str


def load_aws_config() -> AWSConfig:
    """
    .envまたは環境変数からAWS設定を読み込む。
    """

    load_dotenv()

    required_names = [
        "AWS_PROFILE",
        "S3_BUCKET",
    ]

    missing_names = [
        name
        for name in required_names
        if os.getenv(name) is None
    ]

    if missing_names:
        missing_text = ", ".join(
            missing_names
        )

        raise ValueError(
            f"必須の環境変数が"
            f"設定されていません: "
            f"{missing_text}"
        )

    return AWSConfig(
        profile=os.environ["AWS_PROFILE"],
        region=os.getenv(
            "S3_REGION",
            "ap-northeast-1",
        ),
        bucket=os.environ["S3_BUCKET"],
    )