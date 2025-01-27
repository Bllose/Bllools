from bllket.okx.clients.blloseHttpClient import blloseHttpOKE
import logging

logging.basicConfig(level=logging.INFO)
client = blloseHttpOKE()

result = client.get_account(ccy='ETH')
print(result)