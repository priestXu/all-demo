import os
import logging
from pangukitsappdev.api.llms.factory import LLMs

os.environ["SDK_CONFIG_PATH"] = "./llm.properties"
# 打印在命令行（与打印在文件不同时生效）
logging.basicConfig(level=logging.DEBUG)

# 打印在日志文件（与打印在命令行不同时生效）
# logging.basicConfig(level=logging.DEBUG,  # 控制台打印的日志级别
#                     filename='new.log',
#                     filemode='a',
#                    format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s')

# 初始化盘古LLM
llm_api = LLMs.of("pangu")

logging.debug("answer: ", llm_api.ask("你是谁？").answer)
