import unittest
from main import plagiarism_rate, preprocess_text


class TestPreprocessText(unittest.TestCase):
    """测试文本预处理函数"""

    def test_remove_punctuation(self):
        """测试：去除标点符号"""
        raw = "今天天气好，我去看电影。"
        result = preprocess_text(raw)
        self.assertEqual(result, "今天天气好我去看电影")

    def test_remove_whitespace(self):
        """测试：去除空格和换行"""
        raw = "Hello   World\n\nPython"
        result = preprocess_text(raw)
        self.assertEqual(result, "helloworldpython")

    def test_lowercase(self):
        """测试：统一转为小写"""
        raw = "HELLO World"
        result = preprocess_text(raw)
        self.assertEqual(result, "hello world".replace(" ", ""))

    def test_keep_numbers(self):
        """测试：保留数字"""
        raw = "第1章 第2节"
        result = preprocess_text(raw)
        self.assertEqual(result, "第1章第2节")


class TestPlagiarismRate(unittest.TestCase):
    """测试核心查重算法"""

    def test_identical_text(self):
        """测试1：两段文本完全相同 → 应返回 1.0"""
        text = "今天天气真好，我打算下午去看电影。"
        self.assertAlmostEqual(plagiarism_rate(text, text), 1.0)

    def test_completely_different(self):
        """测试2：两段文本完全不同 → 应返回 0.0"""
        text1 = "今天天气真好"
        text2 = "苹果香蕉梨子"
        self.assertAlmostEqual(plagiarism_rate(text1, text2), 0.0)

    def test_empty_both(self):
        """测试3：两个空文本 → 应返回 1.0"""
        self.assertAlmostEqual(plagiarism_rate("", ""), 1.0)

    def test_one_empty(self):
        """测试4：一空一非空 → 应返回 0.0"""
        self.assertAlmostEqual(plagiarism_rate("今天天气好", ""), 0.0)
        self.assertAlmostEqual(plagiarism_rate("", "今天天气好"), 0.0)

    def test_punctuation_interference(self):
        """测试5：抄袭版加入标点符号干扰 → 应仍能识别为高度相似"""
        text1 = "今天天气好我去看电影"
        text2 = "今天天气好，我去看电影！！！"
        self.assertAlmostEqual(plagiarism_rate(text1, text2), 1.0)

    def test_whitespace_interference(self):
        """测试6：抄袭版加入空格干扰 → 应仍能识别为高度相似"""
        text1 = "HelloWorldPython"
        text2 = "H e l l o   W o r l d   P y t h o n"
        self.assertAlmostEqual(plagiarism_rate(text1, text2), 1.0)

    def test_case_interference(self):
        """测试7：抄袭版大小写不同 → 应仍能识别为高度相似"""
        text1 = "HelloWorld"
        text2 = "helloworld"
        self.assertAlmostEqual(plagiarism_rate(text1, text2), 1.0)

    def test_partial_match(self):
        """测试8：部分抄袭 → 相似度应在 0 到 1 之间"""
        text1 = "这是一篇很长的学术论文，讨论了很多问题"
        text2 = "这是一篇很长的学术论文"
        score = plagiarism_rate(text1, text2)
        self.assertTrue(0.0 < score < 1.0)

    def test_reverse_order(self):
        """测试9：语序颠倒 → 应降低相似度，不能是 1.0"""
        text1 = "我爱你中国"
        text2 = "中国爱你我"
        score = plagiarism_rate(text1, text2)
        self.assertLess(score, 1.0)

    def test_long_text_performance(self):
        """测试10：长文本不会崩溃，且能在合理时间内返回结果"""
        text1 = "今天天气真好" * 1000  # 6000 字符
        text2 = "今天天气很好" * 1000
        score = plagiarism_rate(text1, text2)
        self.assertTrue(0.0 <= score <= 1.0)


if __name__ == '__main__':
    unittest.main()