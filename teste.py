from datetime import datetime

formato_string = "%Y-%m-%d %H:%M:%S.%f"
date_token_dt = datetime.strptime("2023-11-27 10:53:30.679043", formato_string)
vida_token = datetime.now() - date_token_dt

print(vida_token.seconds)