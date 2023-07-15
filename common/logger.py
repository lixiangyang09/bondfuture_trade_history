import logging

logging.basicConfig( level=logging.INFO)

#4. 创建控制台handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(lineno)d - %(levelname)s - %(message)s')
cons_handler = logging.FileHandler('log.txt')
cons_handler.setLevel(logging.DEBUG)
cons_handler.setFormatter(formatter)
#5. 添加handler到logger

logger = logging.getLogger(__name__)
logger.addHandler(cons_handler)


