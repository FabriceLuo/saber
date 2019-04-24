#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 mike <mike@mike>
#
# Distributed under terms of the MIT license.

"""

"""
from copy import deepcopy

class CountType(object):
    GENE = 'gene'
    MEDICAL = 'medical'
    JUDICIARY = 'judiciary'
    OTHER = 'other'


class TransactionType(object):
    INCOME = 'income',
    EXPENDITURE = 'expenditure'


class Utils(object):
    @classmethod
    def get_today_date(cls):
        pass

    @classmethod
    def get_date(cls, t):
        return (day, month, year)

class DailyRecord(object):
    pass


class DailyStatistics(object):
    def __init__(self):
        self._records = list()
        income = self.get_default_template()
        expenditure = self.get_default_template()

        self._statistics = dict(TransactionType.INCOME=income,
                                TransactionType.EXPENDITURE=expenditure) 

    @classmethod
    def get_default_template(cls):
        return dict(CountType.GENE=0,
                    CountType.MEDICAL=0,
                    CountType.JUDICIARY=0,
                    CountType.OTHER=0)

    def add_statistics(self, transaction_type, count_type, size):
        self._statistics[transaction_type][count_type] += size

    def add_record(self, record):
        self._records.append(record)
        pass

    def get_statistics(self):
        return deepcopy(self._statistics)


class DailyTable(object):
    def __init__(self, *records):
        self._records = list()

        for record in records:
            self.add_record(record)

    def add_record(self, record):
        self._records.append(record)

    def get_statistics(self):
        daily_statistics = DailyStatistics()
        for record in self._records:
            daily_statistics.add_record(record)

        return daily_statistics

class AccountTable(object):
    def __init__(self, ws=None):
        self._ws = ws

    def get_day_table(self, day, month, year):
        day_table = DailyTable()

        rows = self.find_day_row(day, month, year)
        for row in rows:
            record = self.parse_day_row(row)
            day_table.add_record(record)

        return day_table

    def get_today_table(self):
        (day, month, year) = Utils.get_today_date()
        return self.get_day_table(day, month, year)

    @classmethod
    def parse_day_row(cls, row):
        pass

    def find_day_row(self, day, month, year):
        rows = list()
        for row in self._ws.rows:
            if not self.is_same_day_row(row):
                continue

            rows.append(row)

        return rows

    @classmethod
    def is_day_row(self, row):
        pass

    @classmethod
    def is_same_day_row(self, row, day, month, year=None):
        if not self.is_day_row(row):
            return False

        (row_day, row_month, row_year) = self.parse_day_row(row)
        
        if row_day == day and \
           row_month == month and \
           row_year == year:
            return True

        return False

    @classmethod
    def get_day_column(cls):
        return 'B'

    @classmethod
    def get_month_column(cls):
        return 'A'

    @classmethod
    def get_year_column(cls):
        return None

    def get_table_name(self):
        return self._ws.name

class FoundsRecord(object):
    def __init__(self,
                 account_name,
                 begin_total=0,
                 end_total=0,
                 income=0,
                 expenditure=0):
        self._account_name = account_name
        self._begin_total = begin_total
        self._end_total = end_total
        self._income = income
        self._expenditure = expenditure

    def rotate(self):
        self.update_end_total()

        self._begin_total = self._end_total
        self._income = 0
        self._expenditure = 0

    def update_income(self, size):
        self._income = size
        self.update_end_total()

    def update_expenditure(self, size):
        self._expenditure = size
        self.update_end_total()

    def update_end_total(self):
        self._end_total = self._begin_total + self._income - self._expenditure

    def get_account_name(self):
        return self._account_name

    def get_begin_total(self):
        return self._begin_total

    def get_end_total(self):
        return self._end_total

    def get_income(self):
        return self._income

    def get_expenditure(self):
        return self._expenditure


class FoundsTotalTable(object):
    ACCOUNT_NAME_COLUMN = 'C'
    ACCOUNT_BEGIN_TOTAL_COLUMN = 'I'
    ACCOUNT_END_TOTAL_COLUMN = 'U'
    ACCOUNT_INCOME_TOTAL_COLUMN = 'V'
    ACCOUNT_EXPENDITURE_TOTAL_COLUMN = 'W'

    def __init__(self, ws):
        self._ws = ws

    def verify_founds_total_table(self, ws):
        pass

    def update_today_tables(self, *account_tables):
        for account_table in account_tables:
            self.update_today_table(account_table)

    def update_today_table(self, account_table):
        if self.need_rotate_table():
            self.rotate_table_data()

        self.update_account_data(account_table)

    @classmethod
    def is_account(cls, account_name, row):
        return row[ACCOUNT_NAME_COLUMN] == account_name

    @classmethod
    def is_account_row(cls, row):
        # fixme 判断行是否为账户名称
        if row[ACCOUNT_NAME_COLUMN]:
            return True

        return False

    @classmethod
    def get_record_from_row(cls, row):
        record = FoundsRecord(
            account_name=self.get_record_name(row),
            begin_total=self.get_record_begin_total(row),
            end_total=self.get_record_end_total(row),
            income=self.get_record_income(row),
            expenditure=self.get_record_expenditure(row)
        )
        return record

    @classmethod
    def set_record_to_row(cls, record, row):
        cls.set_record_name(row, record.get_account_name())
        cls.set_record_begin_total(row, record.get_begin_total())
        cls.set_record_end_total(row, record.get_end_total())
        cls.set_record_income(row, record.get_income())
        cls.set_record_expenditure(row, record.get_expenditure())

    def get_account_row(self, account_name):
        for row in self._ws.rows:
            if self.is_account(account_name, row):
                return row

        return None

    @classmethod
    def get_record_name(cls, row):
        return row[ACCOUNT_NAME_COLUMN]

    @classmethod
    def get_record_begin_total(cls, row):
        return row[ACCOUNT_BEGIN_TOTAL_COLUMN]

    @classmethod
    def get_record_end_total(cls, row):
        return row[ACCOUNT_END_TOTAL_COLUMN]

    @classmethod
    def get_record_income(cls, row):
        return row[ACCOUNT_INCOME_TOTAL_COLUMN]

    @classmethod
    def get_record_expenditure(cls, row):
        return row[ACCOUNT_EXPENDITURE_TOTAL_COLUMN]

    @classmethod
    def set_record_name(cls, row, value):
        row[ACCOUNT_NAME_COLUMN] = value

    @classmethod
    def set_record_begin_total(cls, row, value):
        row[ACCOUNT_BEGIN_TOTAL_COLUMN] = value

    @classmethod
    def set_record_end_total(cls, row, value):
        row[ACCOUNT_END_TOTAL_COLUMN] = value

    @classmethod
    def set_record_income(cls, row, value):
        row[ACCOUNT_INCOME_TOTAL_COLUMN] = value

    @classmethod
    def set_record_expenditure(cls, row, value):
        row[ACCOUNT_EXPENDITURE_TOTAL_COLUMN] = value

    def get_today_statistics(self, account_table):
        # 获取今天的记录统计信息
        today_table = account_table.get_today_table()
        today_statistics = today_table.get_statistics()

        # 统计收入和支出
        income = 0
        for i in today_statistics[TransactionType.INCOME].values():
            income += i

        expenditure = 0
        for e in today_statistics[TransactionType.EXPENDITURE].values():
            expenditure += e

        return (income, expenditure)

    def update_account_data(self, account_table):
        account_name = account_table.get_table_name()

        row = self.get_account_row(account_name)
        
        (income, expenditure) = self.get_today_statistics(account_table)
        # 更新记录信息
        record = self.get_record_from_row(row)
        record.update_income(income)
        record.update_expenditure(expenditure)

        self.set_record_to_row(record, row)

    def rotate_table_data(self):
        # 遍历每一条记录，进行轮转
        for row in self._ws.rows:
            if not self.is_account_row(row):
                continue

            record = self.get_record_from_row(row)
            record.rotate()

            self.set_record_to_row(record, row)

    def need_rotate_table(self):
        # 通过对比时间，如果记录的是今天不进行轮转，只进行更新
        return False

    def get_table_date(self):
        pass
