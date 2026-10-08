"""
=============================================================================
  Python 教學：淺拷貝 (Shallow Copy) vs 深拷貝 (Deep Copy)
=============================================================================

核心概念速覽：
1. 直接賦值 (=)：
   - 只是增加一個指向同一個物件的「參照（Reference）」，兩者指向同一塊記憶體。
2. 淺拷貝 (Shallow Copy, copy.copy / list.copy / slice [:])：
   - 複製了「最外層的容器」，但容器裡面的「巢狀物件（如子列表、子字典）」仍然共用相同參照。
   - 修改外層元素不會互相影響，但修改內層可變物件會互相影響！
3. 深拷貝 (Deep Copy, copy.deepcopy)：
   - 遞迴複製「所有層級的物件」。
   - 無論修改外層還是深層巢狀物件，彼此完全獨立、互不干擾。
"""

import copy
import sys

# 確保在 Windows 終端機輸出繁體中文時不出現亂碼
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def print_divider(title: str):
    print("\n" + "=" * 65)
    print(f"  {title}")
    print("=" * 65)


def demo_memory_diagram():
    print_divider("0. 記憶體架構圖解概念")
    diagram = """
    【原始資料】
    original = [ "A", ["B", "C"] ]
                   │         │
                   ▼         ▼
                 "A"      [ "B", "C" ] (子列表記憶體位址: 0x100)
                             ▲
    【淺拷貝 (shallow)】      │
    shallow  = [ "A", ───────┘  <-- 內層指向同一個記憶體 0x100！
                   ▲
                   └── 複製了指標，修改 shallow[1] 時 original 也會被改動

    --------------------------------------------------------------
    【深拷貝 (deep)】
    deep     = [ "A", [ "B", "C" ] ]  <-- 產生全新的子列表 (位址: 0x200)
    深拷貝會遞迴走訪所有層級，全部重新建立獨立的物件！
    """
    print(diagram)


def demo_1_assignment():
    print_divider("1. 直接賦值 (Assignment: b = a)")
    original = [1, 2, [3, 4]]
    assigned = original

    print(f"原始列表 (original): {original}  (記憶體 id: {id(original)})")
    print(f"賦值列表 (assigned): {assigned}  (記憶體 id: {id(assigned)})")
    print("-> 兩者 id 完全相同，代表記憶體中是『同一個物件』！\n")

    print("動作：修改 assigned[0] = 999 以及 assigned[2].append(5)")
    assigned[0] = 999
    assigned[2].append(5)

    print(f"結果 original: {original}")
    print(f"結果 assigned: {assigned}")
    print("-> 結論：修改 assigned，original 也跟著改變。\n")


def demo_2_shallow_copy():
    print_divider("2. 淺拷貝 (Shallow Copy: copy.copy(a) 或 a.copy())")
    original = ["蘋果", "香蕉", ["牛奶", "咖啡"]]
    shallow = copy.copy(original)  # 也可以用 original.copy() 或 original[:]

    print(f"原始列表 (original): {original}  (外層 id: {id(original)})")
    print(f"淺拷貝 (shallow) : {shallow}  (外層 id: {id(shallow)})")
    print(f"-> 外層列表是新建立的 (id 不同): {id(original) != id(shallow)}")
    print(f"-> 但內層子列表 id 卻相同: {id(original[2]) == id(shallow[2])}")
    print(f"   (original[2] id: {id(original[2])}, shallow[2] id: {id(shallow[2])})\n")

    print("【測試 A：修改外層元素】")
    print("動作：shallow[0] = '芭樂'")
    shallow[0] = "芭樂"
    print(f"original: {original}")
    print(f"shallow : {shallow}")
    print("-> 結論：外層元素互不影響，因為外層是獨立的新容器。\n")

    print("【測試 B：修改內層巢狀物件（子列表）】")
    print("動作：shallow[2].append('茶')")
    shallow[2].append("茶")
    print(f"original: {original}")
    print(f"shallow : {shallow}")
    print("-> 警告！內層元素兩者一起被改動了！因為淺拷貝只複製外層，內層依然共用！\n")


def demo_3_deep_copy():
    print_divider("3. 深拷貝 (Deep Copy: copy.deepcopy(a))")
    original = ["蘋果", "香蕉", ["牛奶", "咖啡"]]
    deep = copy.deepcopy(original)

    print(f"原始列表 (original): {original}  (外層 id: {id(original)})")
    print(f"深拷貝 (deep)   : {deep}  (外層 id: {id(deep)})")
    print(f"-> 外層列表 id 是否不同: {id(original) != id(deep)}")
    print(f"-> 內層子列表 id 是否不同: {id(original[2]) != id(deep[2])}")
    print(f"   (original[2] id: {id(original[2])}, deep[2] id: {id(deep[2])})\n")

    print("【測試：同時修改外層元素與內層巢狀物件】")
    print("動作：deep[0] = '水蜜桃', deep[2].append('果汁')")
    deep[0] = "水蜜桃"
    deep[2].append("果汁")

    print(f"original: {original}")
    print(f"deep    : {deep}")
    print("-> 結論：完全獨立！無論改動外層或內層，都不會影響到 original。\n")


def demo_4_dictionary_example():
    print_divider("4. 實際常見陷阱：巢狀字典 (Nested Dictionary)")
    user_profile = {
        "name": "Alice",
        "preferences": {"theme": "dark", "notifications": True},
    }

    # 使用字典自帶的 .copy()（這也是淺拷貝！）
    profile_shallow = user_profile.copy()
    # 使用 deepcopy
    profile_deep = copy.deepcopy(user_profile)

    # 嘗試修改淺拷貝的設定
    profile_shallow["preferences"]["theme"] = "light"

    print("修改 profile_shallow 的 preferences['theme'] 為 'light' 之後：")
    print(f"原始資料 user_profile['preferences']: {user_profile['preferences']}")
    print(f"淺拷貝   profile_shallow['preferences']: {profile_shallow['preferences']}")
    print(f"深拷貝   profile_deep['preferences']: {profile_deep['preferences']}")
    print("-> 提醒：dict.copy() 只淺拷貝第一層，修改內層字典時原字典也會受影響！\n")


def demo_5_summary_table():
    print_divider("5. 總結比較表")
    summary = """
    +-------------------+---------------------+---------------------+
    | 複製方式          | 外層修改是否獨立？   | 內層巢狀修改是否獨立？|
    +-------------------+---------------------+---------------------+
    | 直接賦值 (=)      | 否 (同一物件)       | 否 (同一物件)       |
    | 淺拷貝 (copy)     | 是 (新建外層容器)   | 否 (共用內層參照)   |
    | 深拷貝 (deepcopy) | 是 (新建外層容器)   | 是 (遞迴完全複製)   |
    +-------------------+---------------------+---------------------+

    常見觸發「淺拷貝」的語法：
      - copy.copy(x)
      - list_b = list_a.copy()
      - list_b = list_a[:]
      - dict_b = dict_a.copy()
      - set_b = set_a.copy()
      - list(list_a)

    使用原則：
      - 一維純量資料（例如 [1, 2, 3]）：淺拷貝就足夠且效能更好。
      - 多層巢狀資料（例如包含子列表、子字典或自訂物件）：需要獨立修改時，請務必使用 `copy.deepcopy()`。
    """
    print(summary)


if __name__ == "__main__":
    demo_memory_diagram()
    demo_1_assignment()
    demo_2_shallow_copy()
    demo_3_deep_copy()
    demo_4_dictionary_example()
    demo_5_summary_table()
