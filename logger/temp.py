from custom_logger import CustomLogger


if __name__ == "__main__":
    
    obj = CustomLogger()
    logger = obj.get_logger(__file__)
    a = 10
    logger.info("This is Hello World logging2!", variable=a)

