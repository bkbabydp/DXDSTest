# -*- coding: UTF-8 -*-


import re
from typing import TypeVar, Callable, Iterable, List, Union

from . import func

__author__ = 'David Zhang'

StrOrCallable = TypeVar('StrOrCallable', str, Callable)


class Inflector:
    class Uncountables(set):
        def __init__(self, *args, **kwargs):
            super(Inflector.Uncountables, self).__init__(*args, **kwargs)
            self._regex_set = set()

        def add(self, words):
            """添加不可数单词列表

            :param words:
            :type words: Iterable[str]
            :return:
            :rtype: None
            """
            if func.isiterable(words):
                words_set = {str(w).lower() for w in words}
                self.update(words_set)
                self._regex_set.update(set(map(lambda w: self._to_regex(w), words_set)))

        def delete(self, word):
            """从不可数列表中删除单词

            :param word:
            :type word: str
            :return:
            :rtype: None
            """
            word1 = str(word).lower()
            if word1 in self:
                self.remove(word1)
                reg1 = self._to_regex(word1)
                if reg1 in self._regex_set:
                    self._regex_set.remove(reg1)

        def isuncountable(self, term):
            """判断word是否包含不可数单词形式

            :param term:
            :type term: str
            :return:
            :rtype: bool
            """
            for r in self._regex_set:
                m = re.match(r, term)
                if m:
                    result = True
                    break
            else:
                result = False

            return result

        # private

        @staticmethod
        def _to_regex(word):
            """根据word生成对应的唯一正则表达式

            :param word:
            :type word: str
            :return:
            :rtype: str
            """
            return r'(?i)\b%s\Z' % re.escape(word)

    def __init__(self):
        self._plurals_list = []  # type: List[Union[str, Callable]]
        self._singulars_list = []  # type: List[Union[str, Callable]]
        self._uncountables_set = self.Uncountables()
        self._humans_list = []  # type: List[Union[str, Callable]]
        self._acronyms_dict = {}
        self._acronym_regex = r'(?=a)b'
        self._init_rules()

    def _init_rules(self) -> None:
        self._acronym('API', 'HTML', 'HTTP', 'JSON', 'RESTful', 'W3C', 'PhD', 'RoR', 'SSL')

        self._plural(r'$', 's')
        self._plural(r'(?i)s$', 's')
        self._plural(r'(?i)^(ax|test)is$', r'\1es')
        self._plural(r'(?i)(octop|vir)us$', r'\1i')
        self._plural(r'(?i)(octop|vir)i$', r'\1i')
        self._plural(r'(?i)(alias|status)$', r'\1es')
        self._plural(r'(?i)(bu)s$', r'\1ses')
        self._plural(r'(?i)(buffal|tomat)o$', r'\1oes')
        self._plural(r'(?i)([ti])um$', r'\1a')
        self._plural(r'(?i)([ti])a$', r'\1a')
        self._plural(r'(?i)sis$', 'ses')
        self._plural(r'(?i)(?:([^f])fe|([lr])f)$', r'\1\2ves')
        self._plural(r'(?i)(hive)$', r'\1s')
        self._plural(r'(?i)([^aeiouy]|qu)y$', r'\1ies')
        self._plural(r'(?i)(x|ch|ss|sh)$', r'\1es')
        self._plural(r'(?i)(matr|vert|ind)(?:ix|ex)$', r'\1ices')
        self._plural(r'(?i)^(m|l)ouse$', r'\1ice')
        self._plural(r'(?i)^(m|l)ice$', r'\1ice')
        self._plural(r'(?i)^(ox)$', r'\1en')
        self._plural(r'(?i)^(oxen)$', r'\1')
        self._plural(r'(?i)(quiz)$', r'\1zes')

        self._singular(r's$', '')
        self._singular(r'(?i)(ss)$', r'\1')
        self._singular(r'(?i)(n)ews$', r'\1ews')
        self._singular(r'(?i)([ti])a$', r'\1um')
        self._singular(r'(?i)((a)naly|(b)a|(d)iagno|(p)arenthe|(p)rogno|(s)ynop|(t)he)(sis|ses)$', r'\1sis')
        self._singular(r'(?i)(^analy)(sis|ses)$', r'\1sis')
        self._singular(r'(?i)([^f])ves$', r'\1fe')
        self._singular(r'(?i)(hive)s$', r'\1')
        self._singular(r'(?i)(tive)s$', r'\1')
        self._singular(r'(?i)([lr])ves$', r'\1f')
        self._singular(r'(?i)([^aeiouy]|qu)ies$', r'\1y')
        self._singular(r'(?i)(s)eries$', r'\1eries')
        self._singular(r'(?i)(m)ovies$', r'\1ovie')
        self._singular(r'(?i)(x|ch|ss|sh)es$', r'\1')
        self._singular(r'(?i)^(m|l)ice$', r'\1ouse')
        self._singular(r'(?i)(bus)(es)?$', r'\1')
        self._singular(r'(?i)(o)es$', r'\1')
        self._singular(r'(?i)(shoe)s$', r'\1')
        self._singular(r'(?i)(cris|test)(is|es)$', r'\1is')
        self._singular(r'(?i)^(a)x[ie]s$', r'\1xis')
        self._singular(r'(?i)(octop|vir)(us|i)$', r'\1us')
        self._singular(r'(?i)(alias|status)(es)?$', r'\1')
        self._singular(r'(?i)^(ox)en', r'\1')
        self._singular(r'(?i)(vert|ind)ices$', r'\1ex')
        self._singular(r'(?i)(matr)ices$', r'\1ix')
        self._singular(r'(?i)(quiz)zes$', r'\1')
        self._singular(r'(?i)(database)s$', r'\1')

        self._irregular('person', 'people')
        self._irregular('man', 'men')
        self._irregular('child', 'children')
        self._irregular('sex', 'sexes')
        self._irregular('move', 'moves')
        self._irregular('zombie', 'zombies')

        self._uncountable(
            'equipment', 'information', 'rice', 'money', 'species',
            'series', 'fish', 'sheep', 'jeans', 'police'
        )

    def pluralize(self, term):
        """获取单词的复数形式
        范例：
            pluralize('post')             # => "posts"
            pluralize('octopus')          # => "octopi"
            pluralize('sheep')            # => "sheep"
            pluralize('words')            # => "words"
            pluralize('CamelOctopus')     # => "CamelOctopi"

        :param term:
        :type term: str
        :return:
        :rtype: str
        """
        return self._apply_inflections(term, self._plurals_list)

    def singularize(self, term):
        """获取单词的单数形式
        范例：
            singularize('posts')            # => "post"
            singularize('octopi')           # => "octopus"
            singularize('sheep')            # => "sheep"
            singularize('word')             # => "word"
            singularize('CamelOctopi')      # => "CamelOctopus"

        :param term:
        :type term: str
        :return:
        :rtype: str
        """
        return self._apply_inflections(term, self._singulars_list)

    def camelize(self, term, uppercase_first_letter=True):
        """获取字符串的【驼峰表示法】形式（每个单词的只有首字母大写，或者整个字符串的首字母小写）
        范例：
            camelize('active_model')                # => "ActiveModel"
            camelize('active_model', false)         # => "activeModel"
            camelize('active_model/errors')         # => "ActiveModel::Errors"
            camelize('active_model/errors', false)  # => "activeModel::Errors"

        :param term:
        :type term: str
        :param uppercase_first_letter:
        :type uppercase_first_letter: bool
        :return:
        :rtype: str
        """
        term1 = str(term)
        if uppercase_first_letter:
            term1 = re.sub(
                pattern=r'^[a-z\d]*',
                repl=lambda m: self._acronyms_dict[m[0]] if m[0] in self._acronyms_dict else m[0].capitalize(),
                string=term1,
                count=1
            )
        else:
            term1 = re.sub(
                pattern=r'^(?:%s(?=\b|[A-Z_])|\w)' % self._acronym_regex,
                repl=lambda m: m[0].lower(),
                string=term1,
                count=1
            )

        term1 = re.sub(
            pattern=r'(?i)(?:_|(\/))([a-z\d]*)',
            repl=lambda m: '%s%s' % (
                m[1],
                self._acronyms_dict[m[2]] if m[2] in self._acronyms_dict else m[2].capitalize()
            ),
            string=term1
        )

        term1 = re.sub(pattern='/', repl='::', string=term1)

        return term1

    def underscore(self, camel_cased_word):
        """获取字符串的【下划线表示法】形式（所有单词小写，单词之间用下划线连接）
        范例：
            underscore('ActiveModel')         # => "active_model"
            underscore('ActiveModel::Errors') # => "active_model/errors"

        :param camel_cased_word:
        :type camel_cased_word: str
        :return:
        :rtype: str
        """
        if re.match(pattern=r'[A-Z-]|::', string=camel_cased_word) is None:
            result = camel_cased_word
        else:
            word = re.sub(pattern='::', repl='/', string=str(camel_cased_word))
            word = re.sub(
                pattern=r'(?:(?<=([A-Za-z\d]))|\b)(%s)(?=\b|[^a-z])' % self._acronym_regex,
                repl=lambda m: '%s_%s' % (m[1], m[2].lower()),
                string=word
            )
            word = re.sub(pattern=r'([A-Z\d]+)([A-Z][a-z])', repl=r'\1_\2', string=word)
            word = re.sub(pattern=r'([a-z\d])([A-Z])', repl=r'\1_\2', string=word)
            word = re.sub(pattern='-', repl='_', string=word)
            result = word.lower()

        return result

    def humanize(self, lower_case_and_underscored_word, capitalize=False):
        """获取【下划线表达式】的【英文可读模式】（单词之间用空格分割，单词大小写根据英文文章书写习惯，适合作为说明或注释）
        范例：
            humanize('employee_salary')              # => "Employee salary"
            humanize('author_id')                    # => "Author"
            humanize('author_id', capitalize: false) # => "author"
            humanize('_id')                          # => "Id"

            or:
            acronym('SSL')
            humanize('ssl_error') # => "SSL error"

        :param lower_case_and_underscored_word:
        :type lower_case_and_underscored_word: str
        :param capitalize:
        :type capitalize: bool
        :return:
        :rtype: str
        """
        result = str(lower_case_and_underscored_word)

        for p, r in self._humans_list:
            result, n = re.subn(pattern=p, repl=r, string=result)
            if n > 0:
                break

        result = re.sub(pattern=r'\A_+', repl='', string=result, count=1)
        result = re.sub(pattern=r'_id\z', repl='', string=result, count=1)
        result = re.sub(pattern='_', repl=' ', string=result)

        result = re.sub(
            pattern=r'(?i)([a-z\d]*)',
            repl=lambda m: self._acronyms_dict[m[0]] if m[0] in self._acronyms_dict else m[0].lower(),
            string=result
        )

        if capitalize:
            result = re.sub(
                pattern=r'\A\w',
                repl=lambda m: m[0].upper(),
                string=result
            )

        return result

    @staticmethod
    def upcase_first(term):
        """设置整个字符串首字母为大写
        范例：
            upcase_first('what a Lovely Day') # => "What a Lovely Day"
            upcase_first('w')                 # => "W"
            upcase_first('')                  # => ""

        :param term:
        :type term: str
        :return:
        :rtype: str
        """
        term1 = str(term)
        result = '%s%s' % (term1[0].upper(), term1[1:]) if term1 else ''

        return result

    def titleize(self, word):
        """获取对应的标题／说明形式
        范例：
            titleize('man from the boondocks')   # => "Man From The Boondocks"
            titleize('x-men: the last stand')    # => "X Men: The Last Stand"
            titleize('TheManWithoutAPast')       # => "The Man Without A Past"
            titleize('raiders_of_the_lost_ark')  # => "Raiders Of The Lost Ark"

        :param word:
        :type word: str
        :return:
        :rtype: str
        """
        return re.sub(
            pattern=u'\\b(?<![\'’`])[a-z]',
            repl=lambda m: m[0].capitalize(),
            string=self.humanize(self.underscore(word))
        )

    def tableize(self, class_name):
        """根据类名生成对应的数据库表名
        范例：
            tableize('RawScaledScorer') # => "raw_scaled_scorers"
            tableize('ham_and_egg')     # => "ham_and_eggs"
            tableize('fancyCategory')   # => "fancy_categories"

        :param class_name:
        :type class_name: str
        :return:
        :rtype: str
        """
        return self.pluralize(self.underscore(class_name))

    def classify(self, table_name):
        """根据数据库表名生成对应的类名
        范例：
            classify('ham_and_eggs') # => "HamAndEgg"
            classify('posts')        # => "Post"

            but:
            classify('calculus')     # => "Calculus"

        :param table_name:
        :type table_name: str
        :return:
        :rtype: str
        """
        return self.camelize(self.singularize(re.sub(
            pattern=r'.*\.',
            repl='',
            string=str(table_name),
            count=1
        )))

    @staticmethod
    def dasherize(underscored_word):
        """从【下划线表示法】转换为【横线表示法】
        范例：
            dasherize('puni_puni') # => "puni-puni"

        :param underscored_word:
        :type underscored_word: str
        :return:
        :rtype: str
        """
        return re.sub(pattern='_', repl='-', string=underscored_word)

    # private

    def _acronym(self, *words):
        """定义单词缩写形式
        范例：
            acronym('HTTP')
            camelize('my_http_delimited') # => 'MyHTTPDelimited'
            camelize('https')             # => 'Https', not 'HTTPs'
            underscore('HTTPS')           # => 'http_s', not 'https'

            acronym('HTTPS')
            camelize('https')   # => 'HTTPS'
            underscore('HTTPS') # => 'https'

        :param word: 缩写单词
        :type word: str
        :return:
        :rtype: None
        """
        for w in words:
            self._acronyms_dict[w.lower()] = w
        self._acronym_regex = '|'.join(self._acronyms_dict.values())

    def _human(self, pattern, replacement):
        """添加人工转换规则
        范例：
            human(r'(?i)_cnt$', '\1_count'
            human('legacy_col_person_name', 'Name')

        :param pattern: 正则表达式字符串
        :type pattern: str
        :param replacement: 替换字符串或者替换函数
        :type replacement: str | Callable
        :return:
        :rtype: None
        """
        self._humans_list.insert(0, [pattern, replacement])

    def _uncountable(self, *words):
        """添加不可数单词
        范例：
            uncountable('equipment', 'information')

        :param words: 不可数单词列表
        :type words: Iterable[str]
        :return:
        :rtype: None
        """
        self._uncountables_set.add(words)

    def _plural(self, pattern, replacement):
        """添加复数转换规则
        范例：
            plural(r'(?i)(buffal|tomat)o$', '\1oes')

        :param pattern: 正则表达式字符串
        :type pattern: str
        :param replacement: 替换字符串或者替换函数
        :type replacement: str | Callable
        :return:
        :rtype: None
        """
        if func.isstr(pattern):
            self._uncountables_set.delete(pattern)

        if func.isstr(replacement):
            self._uncountables_set.delete(replacement)

        # 后添加的规则，优先级更高
        self._plurals_list.insert(0, [pattern, replacement])

    def _singular(self, pattern, replacement):
        """添加单数转换规则
        范例：
            singular(r'(?i)(cris|test)(is|es)$', '\1is')

        :param pattern: 正则表达式字符串
        :type pattern: str
        :param replacement: 替换字符串或者替换函数
        :type replacement: str | Callable
        :return:
        :rtype: None
        """
        if func.isstr(pattern):
            self._uncountables_set.delete(pattern)

        if func.isstr(replacement):
            self._uncountables_set.delete(replacement)

        # 后添加的规则，优先级更高
        self._singulars_list.insert(0, [pattern, replacement])

    def _irregular(self, singular, plural):
        """添加不规则单词语法规则
        范例：
            irregular('person', 'people')
            irregular('octopus', 'octopi')

        :param singular: 单数形式
        :type singular: str
        :param plural: 复数形式
        :type plural: str
        :return:
        :rtype: None
        """
        if func.isstr(singular) and func.isstr(plural):
            self._uncountables_set.delete(singular)
            self._uncountables_set.delete(plural)

            def get_repl(replacement):
                """根据替换字符串，返回re.sub的repl函数

                :param replacement:
                :type replacement: str | None
                :return:
                :rtype: Callable
                """

                def repl(match):
                    """re.sub的repl函数

                    :param match: re.sub传入的Match对象
                    :type match: _sre.SRE_Match | None
                    :return: 对应的replacement字符串
                    :rtype: str
                    """

                    s2 = replacement
                    s1 = match.group(0)
                    if s1:
                        s1_0 = s1[0]
                        if s2:
                            s2_0 = s2[0]

                            # 将替换的单词首字母大小写与原单词进行统一
                            s2_0 = s2_0.upper() if s1_0.upper() == s1_0 else s2_0.lower()

                            s2 = '%s%s' % (s2_0, s2[1:])

                    return s2

                return repl

            self._plural(r'(?i)%s$' % singular, get_repl(plural))
            self._singular(r'(?i)%s$' % plural, get_repl(singular))

    def _apply_inflections(self, term, rules):
        """

        :param term:
        :type term: str
        :param rules:
        :type rules: List[Union[str | Callable]]
        :return:
        :rtype: str
        """
        result = str(term)

        if result and not self._uncountables_set.isuncountable(result):
            for p, r in rules:
                result, n = re.subn(pattern=p, repl=r, string=result)
                if n > 0:
                    break

        return result
