import json
import os

INPUT_FILE = "orders.json"
OUTPUT_FILE = "output_orders.json"

def load_data(filename: str) -> list:
    if not os.path.exists(filename):
        return []
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_orders(filename: str, orders: list) -> None:
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(orders, f, ensure_ascii=False, indent=4)

# 計算顧客要付的總金額
def calculate_order_total(order: dict) -> int:
    total = 0
    for items in order["items"]:
        total += items["price"] * items["quantity"]
    return total

# 處理出餐
def process_order(orders: list) -> tuple:
    print("\n======== 待處理訂單列表 ========")
    for i in range(0, len(orders), 1):
        print("{0}. 訂單編號: {1} - 客戶: {2}"
              .format(i+1, orders[i]["order_id"], orders[i]["customer"]))
    while True:
        try:
            num = int(input("請選擇要出餐的訂單編號 (輸入數字或按 Enter 取消):"))
            if num <= 0 or num > len(orders):
                print("=> 錯誤：請輸入有效的數字")
                continue
            print("=> 訂單 {0} 已出餐完成".format(orders[num-1]["order_id"]))
            break
        except ValueError:
            print("=> 錯誤：請輸入有效的數字")
            continue

    print("出餐訂單詳細資料：\n")
    print("==================== 出餐訂單 ====================")
    print("訂單編號: {0}".format(orders[num-1]["order_id"]))
    print("客戶姓名: {0}".format(orders[num-1]["customer"]))
    print("--------------------------------------------------")
    print("{:<8}\t{:<4}\t{:<4}\t{:<6}"
            .format("商品名稱", "單價", "數量", "小計"))
    print("--------------------------------------------------")

    # 顯示每一個訂單項目
    for j in range(len(orders[i]["items"])):
        items = orders[i]["items"][j]
        subtotal = items["price"] * items["quantity"]
        print("{:<12}\t{:<6,}\t{:<6}\t{:<6,}"
                .format(items["name"], items["price"],
                        items["quantity"], subtotal))

    print("--------------------------------------------------")
    print("訂單總額: {:,}".format(calculate_order_total(orders[i])))
    print("==================================================\n")


    # 新增output_orders資料
    ok_orders = load_data(OUTPUT_FILE)
    ok_orders.append(orders[num-1])
    save_orders(OUTPUT_FILE, ok_orders)

    # 刪除orders.json資料
    orders.pop(num-1)

# 新增訂單
def add_order(orders: list) -> str:
    order_id = input("請輸入訂單編號：").upper()

    # 用any檢查是否已經有這個訂單編號
    if any(order["order_id"] == order_id for order in orders):
        return f"=> 錯誤：訂單編號 {order_id} 已存在！"

    customer = input("請輸入顧客姓名：")
    items = []

    while True:
        name = input("請輸入訂單項目名稱（輸入空白結束）：")
        if name == "" or name == " ":
            if len(items) == 0:
                print("=> 至少需要一個訂單項目")
                continue
            else:
                orders.append({"order_id": order_id,
                               "customer": customer,
                               "items": items})
                return f"=> 訂單 {order_id} 已新增！"

        while True:
            try:
                price = int(input("請輸入價格："))
                if price < 0:
                    print("=> 錯誤：價格不能為負數，請重新輸入")
                    continue
                break
            except ValueError:
                print("=> 錯誤：價格或數量必須為整數，請重新輸入")
                continue

        while True:
            try:
                quantity = int(input("請輸入數量："))
                if quantity <= 0:
                    print("=> 錯誤：數量必須為正整數，請重新輸入")
                    continue
                break
            except ValueError:
                print("=> 錯誤：價格或數量必須為整數，請重新輸入")
                continue
        items.append({"name": name, "price": price, "quantity": quantity})

# 印出報表
def print_order_report(data, title="訂單報表", single=False):
    print(f"\n==================== {title} ====================")

    for i in range(0, len(data), 1):
        #calculate_order_total(data[i]["items"])
        print("訂單 #{0}".format(i+1))
        print("訂單編號: {0}".format(data[i]["order_id"]))
        print("客戶姓名: {0}".format(data[i]["customer"]))
        print("--------------------------------------------------")

        print("{:<8}\t{:<4}\t{:<4}\t{:<6}"
              .format("商品名稱", "單價", "數量", "小計"))
        print("--------------------------------------------------")

        # 顯示每一個訂單項目
        for j in range(len(data[i]["items"])):
            items = data[i]["items"][j]
            subtotal = items["price"] * items["quantity"]
            print("{:<12}\t{:<6,}\t{:<6}\t{:<6,}"
                  .format(items["name"], items["price"],
                          items["quantity"], subtotal))

        print("--------------------------------------------------")
        print("訂單總額: {:,}".format(calculate_order_total(data[i])))
        print("==================================================\n")

def main():
    print("***************選單***************")
    print("1. 新增訂單")
    print("2. 顯示訂單報表")
    print("3. 出餐處理")
    print("4. 離開")
    print("**********************************")
    choice = input("請選擇操作項目(Enter 離開)：")
    orders = load_data(INPUT_FILE)

    if choice == "1":
        print(add_order(orders))
    elif choice == "2":
        # 因為我們沒在print_order_report傳回值，
        # 所以直接進去print_order_report執行即可，若加上print我們會得到None
        print_order_report(orders)
    elif choice == "3":
        process_order(orders)
    # choice == "" >>> 直接Enter離開
    elif choice == "4" or choice == "":
        exit()
    else:
        print("=> 請輸入有效的選項（1-4）")
        main()

    save_orders(INPUT_FILE, orders)

main()
