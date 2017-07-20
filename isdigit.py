#!/usr/bin/env python
# coding: utf-8

def toNumber(num_str):
    """文字列を適切な型の数値に変換する"""
    try:
        value = float(num_str)
        if value == int(value):
            return int(value)
    except ValueError:
        return 0
    