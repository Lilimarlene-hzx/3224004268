import argparse
import sys
from difflib import SequenceMatcher
from pathlib import Path


def read_text(path: Path) -> str:
    """读取文件"""
    return path.read_text(encoding="utf-8")


def plagiarism_rate(original: str, copy: str) -> float:
    """直接使用 SequenceMatcher 对比原始文本"""
    if not original or not copy:
        return 0.0
    return SequenceMatcher(None, original, copy, autojunk=False).ratio()


def main() -> None:
    parser = argparse.ArgumentParser(description="论文查重")
    parser.add_argument("original", type=Path, help="原文路径")
    parser.add_argument("copy", type=Path, help="抄袭版路径")
    parser.add_argument("answer", type=Path, help="结果输出路径")
    args = parser.parse_args()

    original_text = read_text(args.original)
    copy_text = read_text(args.copy)
    rate = plagiarism_rate(original_text, copy_text)

    # 将结果写入ans.txt文件中，保留两位小数
    args.answer.write_text(f"{rate:.2f}", encoding="utf-8")


if __name__ == "__main__":
    main()