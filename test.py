# -*- coding: utf8 -*-
from financial_save_data import FinancialStatementGet

result = FinancialStatementGet(2330, 'C:\\MMM\\FinancialData\\', 1, 1)
print result.financial_statement_get()