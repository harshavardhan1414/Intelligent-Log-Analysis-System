import sys

from src.utils.exception import CustomException

try:

    a=10

    b=0

    c=a/b

except Exception as e:

    raise CustomException(e,sys)