import argparse  # noqa: I001
import re  #【V3新增】
import sys
import hashlib  
from difflib import SequenceMatcher
from pathlib import Path


def read_text(path: Path) -> str:
    """Read a UTF-8 text file, including files with a UTF-8 BOM."""
    if not path.is_absolute():
        raise ValueError(f"路径必须是绝对路径: {path}")
    if not path.exists():
        raise FileNotFoundError(f"文件不存在: {path}")
    if not path.is_file():
        raise OSError(f"路径不是有效的文件: {path}")
    try:
        return path.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeError) as e:
        raise OSError(f"读取文件失败 {path}: {e}") from e


def preprocess_text(text: str) -> str:
    """Remove punctuation and whitespace, preserving Chinese, letters, and digits."""
    cleaned = re.sub(r"[^\u3400-\u9fffA-Za-z0-9]", "", text)
    return cleaned.lower()



def plagiarism_rate(original: str, copy: str) -> float:
    """【优化版】自适应切换：短文本精确匹配，长文本分块哈希"""
    orig_clean = preprocess_text(original)
    copy_clean = preprocess_text(copy)

    if not orig_clean and not copy_clean:
        return 1.0
    if not orig_clean or not copy_clean:
        return 0.0

    # 策略切换：5000字符为阈值
    if len(orig_clean) < 5000 or len(copy_clean) < 5000:
        # 短文本：使用精确算法，保证精度
        return SequenceMatcher(None, orig_clean, copy_clean, autojunk=False).ratio()

    # 长文本：使用分块哈希，保证速度
    BLOCK_SIZE = 50

    def make_blocks(text):
        # 步长设为块大小的一半，避免边界错位导致漏检
        step = BLOCK_SIZE // 2
        return [text[i:i+BLOCK_SIZE] for i in range(0, len(text) - BLOCK_SIZE + 1, step)]

    blocks_orig = make_blocks(orig_clean)
    blocks_copy = make_blocks(copy_clean)

    # 构建原文哈希表
    hash_table = set()
    for block in blocks_orig:
        hash_table.add(hashlib.md5(block.encode('utf-8')).hexdigest())

    # 统计命中块数
    matched = 0
    for block in blocks_copy:
        if hashlib.md5(block.encode('utf-8')).hexdigest() in hash_table:
            matched += 1

    return matched / len(blocks_copy) if blocks_copy else 0.0


def main() -> None:
    parser = argparse.ArgumentParser(description="论文查重扩展版")
    parser.add_argument("original", type=Path, help="原文路径")
    parser.add_argument("copy", type=Path, help="抄袭版路径")
    parser.add_argument("answer", type=Path, help="结果输出路径")
    args = parser.parse_args()

    if not args.original.is_absolute() or not args.copy.is_absolute() or not args.answer.is_absolute():
        parser.error("原文、抄袭版和答案路径都必须是绝对路径")

    try:
        original_text = read_text(args.original)
        copy_text = read_text(args.copy)
        rate = plagiarism_rate(original_text, copy_text)

        args.answer.parent.mkdir(parents=True, exist_ok=True)
        args.answer.write_text(f"{rate:.2f}", encoding="utf-8")

    except (OSError, ValueError) as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)  # 优雅退出，状态码非0


if __name__ == "__main__":
    main()