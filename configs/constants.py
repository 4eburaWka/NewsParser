LOCAL_ENV, DEV_ENV, PROD_ENV = 'local', 'dev', 'prod'

with open("configs/prompts/is_duplicate.txt") as file:
    IS_DUPLICATE_PROMPT = file.read()
