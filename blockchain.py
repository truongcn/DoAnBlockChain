import hashlib
import json
import time

class Block:
    def __init__(self, index, previous_hash, timestamp, data, hash):
        self.index = index  # Vị trí của khối trong chuỗi
        self.previous_hash = previous_hash  # Hash của khối trước đó
        self.timestamp = timestamp  # Thời gian tạo khối
        self.data = data  # Dữ liệu lưu trong khối (ví dụ: giao dịch)
        self.hash = hash  # Hash của khối hiện tại

    @staticmethod
    def calculate_hash(index, previous_hash, timestamp, data):
        # Tạo hash từ các thuộc tính của khối
        value = str(index) + str(previous_hash) + str(timestamp) + str(data)
        return hashlib.sha256(value.encode('utf-8')).hexdigest()

class Blockchain:
    def __init__(self):
        # Khởi tạo chuỗi với khối genesis (khối đầu tiên)
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        # Tạo khối genesis
        timestamp = time.time()
        genesis_block = Block(0, "0", timestamp, "Genesis Block", "")
        genesis_block.hash = Block.calculate_hash(0, "0", timestamp, "Genesis Block")
        self.chain.append(genesis_block)

    def get_latest_block(self):
        # Lấy khối mới nhất trong chuỗi
        return self.chain[-1]

    def add_block(self, data):
        # Thêm khối mới vào chuỗi
        previous_block = self.get_latest_block()
        index = previous_block.index + 1
        timestamp = time.time()
        hash = Block.calculate_hash(index, previous_block.hash, timestamp, data)
        new_block = Block(index, previous_block.hash, timestamp, data, hash)
        self.chain.append(new_block)

    def is_chain_valid(self):
        # Kiểm tra tính hợp lệ của chuỗi
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]

            # Kiểm tra hash của khối hiện tại
            if current_block.hash != Block.calculate_hash(
                current_block.index,
                current_block.previous_hash,
                current_block.timestamp,
                current_block.data
            ):
                return False

            # Kiểm tra liên kết với khối trước
            if current_block.previous_hash != previous_block.hash:
                return False
        return True

# Thử nghiệm Blockchain
if __name__ == "__main__":
    # Tạo một blockchain mới
    my_blockchain = Blockchain()

    # Thêm một số khối
    my_blockchain.add_block("Giao dịch 1: A gửi B 10 coin")
    my_blockchain.add_block("Giao dịch 2: B gửi C 5 coin")

    # In thông tin chuỗi
    for block in my_blockchain.chain:
        print(f"Index: {block.index}")
        print(f"Previous Hash: {block.previous_hash}")
        print(f"Timestamp: {block.timestamp}")
        print(f"Data: {block.data}")
        print(f"Hash: {block.hash}")
        print("---")

    # Kiểm tra tính hợp lệ
    print(f"Blockchain hợp lệ? {my_blockchain.is_chain_valid()}")

    # Thử giả mạo dữ liệu
    my_blockchain.chain[1].data = "Giao dịch giả mạo"
    print(f"Blockchain hợp lệ sau khi giả mạo? {my_blockchain.is_chain_valid()}")