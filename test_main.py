import unittest

from main import plagiarism_rate, preprocess_text


class TestPlagiarismChecker(unittest.TestCase):

    def test_identical(self):
        """测试1：完全相同"""
        self.assertAlmostEqual(plagiarism_rate("今天天气好", "今天天气好"), 1.0)

    def test_completely_different(self):
        """测试2：完全不同"""
        self.assertAlmostEqual(plagiarism_rate("今天天气好", "苹果香蕉梨"), 0.0)

    def test_empty_both(self):
        """测试3：两个空文件"""
        self.assertAlmostEqual(plagiarism_rate("", ""), 1.0)

    def test_one_empty(self):
        """测试4：其中一个为空"""
        self.assertAlmostEqual(plagiarism_rate("今天天气好", ""), 0.0)

    def test_punctuation_interference(self):
        """测试5：标点符号干扰（应该被预处理过滤）"""
        text1 = "今天天气好，我去看电影。"
        text2 = "今天天气好  我去看电影！！！"
        self.assertAlmostEqual(plagiarism_rate(text1, text2), 1.0)

    def test_whitespace_interference(self):
        """测试6：空格干扰"""
        text1 = "Hello World"
        text2 = "H e l l o   W o r l d"
        self.assertAlmostEqual(plagiarism_rate(text1, text2), 1.0)

    def test_case_insensitive(self):
        """测试7：大小写干扰"""
        text1 = "Hello World"
        text2 = "hello world"
        self.assertAlmostEqual(plagiarism_rate(text1, text2), 1.0)

    def test_partial_match(self):
        """测试8：部分匹配（只抄了一半）"""
        text1 = "这是一篇很长的论文"
        text2 = "这是一篇很短的论文"
        score = plagiarism_rate(text1, text2)
        self.assertTrue(0.5 < score < 1.0)

    def test_preprocess_special_chars(self):
        """测试9：预处理函数专门测试"""
        raw = "Hello, World! 123。"
        processed = preprocess_text(raw)
        self.assertEqual(processed, "helloworld123")

    def test_reverse_order(self):
        """测试10：语序颠倒（LCS会降低相似度）"""
        text1 = "我爱你"
        text2 = "你爱我"
        score = plagiarism_rate(text1, text2)
        self.assertLess(score, 1.0)  


if __name__ == '__main__':
    unittest.main()