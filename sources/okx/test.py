import okx.Trade as Trade

apikey = "085a870b-73a6-4bfd-8479-b7389d042d69"
secretkey = "26079B859BF71FC3920BC4A63A13F472"
IP = "113.73.230.105"

import okx.PublicData as PublicData

  flag = "1"  # live trading: 0, demo trading: 1

  PublicDataAPI = PublicData.PublicAPI(flag=flag)

  result = PublicDataAPI.get_instruments(
      instType="SPOT"
  )
  print(result)