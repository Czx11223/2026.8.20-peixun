from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # 大模型（默认 DeepSeek；无密钥时自动降级为内置 mock，保证可运行）
    model_name: str = "deepseek-chat"
    api_key: str = ""
    base_url: str = "https://api.deepseek.com/v1"
    temperature: float = 0.7
    max_tokens: int = 2048

    # 数据库
    db_path: str = "data/mianzhi.db"

    # 是否启用 ChromaDB 向量检索（False 时退化为关键字匹配）
    use_vector: bool = False

    model_config = SettingsConfigDict(env_prefix="MIANZHI_", env_file=".env", extra="ignore")


settings = Settings()
