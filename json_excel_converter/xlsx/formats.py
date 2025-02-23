class Format:
    def __init__(self, fmt=None, column_index=None, row_index=None):
        self.fmt = fmt or {}
        self.column_index = column_index
        self.row_index = row_index

    def data_format(self, cell_data, rowidx, colidx, first, last):
        return self.fmt


class Bold(Format):
    @classmethod
    def data_format(cls, cell_data, rowidx, colidx, first, last):
        return {
            'bold': True
        }


class Centered(Format):
    @classmethod
    def data_format(cls, cell_data, rowidx, colidx, first, last):
        return {
            'align': 'center',
            'valign': 'vcenter'
        }


class LastUnderlined(Format):
    @classmethod
    def data_format(cls, cell_data, rowidx, colidx, first, last):
        if last:
            return {
                'bottom': 1
            }
        return {}


class ColumnBorder(Format):
    @classmethod
    def data_format(cls, cell_data, rowidx, colidx, first, last):
        return {
            'left': 1,
            'right': 1
        }
