import logging
import os
import pandas as pd
from bllket.okx.clients.blloseHttpClient import blloseHttpOKE

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_candlestick_data(instId='BTC-USDT', bar='1H'):
    """
    从 blloseHttpOKE 客户端获取 K 线数据
    """
    try:
        client = blloseHttpOKE()
        logging.info(f"Fetching candlestick data for {instId} with bar {bar}...")
        return client.marked_candlesticks(instId=instId, bar=bar)
    except Exception as e:
        logging.error(f"Failed to fetch candlestick data: {e}")
        raise

def save_to_csv(data, file_path):
    """
    将数据保存为 CSV 文件
    """
    try:
        # 直接使用 Pandas 的 DataFrame 构造函数
        df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df.to_csv(file_path, index=False)
        logging.info(f"Data successfully saved to {file_path}")
    except Exception as e:
        logging.error(f"Failed to save data to CSV: {e}")
        raise

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    # 定义文件路径
    csv_file_path = os.path.join("data", "crypto_data.csv")
    
    # 确保目录存在
    os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)
    
    try:
        # 获取 K 线数据
        candlestick_data = fetch_candlestick_data(instId='BTC-USDT', bar='1H')
        
        # 处理数据
        processed_data = [
            {
                'timestamp': data[0],
                'open': data[1],
                'high': data[2],
                'low': data[3],
                'close': data[4],
                'volume': data[5]
            }
            for data in candlestick_data
        ]
        
        # 保存为 CSV 文件
        save_to_csv(processed_data, csv_file_path)
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()