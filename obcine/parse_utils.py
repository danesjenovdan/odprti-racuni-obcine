import xlrd
import time
import requests
from django.db import transaction


class XLSXAppraBudget(object):
    def __init__(self, document, model, month=None):
        self.municipality = document.municipality
        self.year = document.year
        self.model = model
        self.document_object = document
        self.month = month

    def prepare_moodel(self, name, code, order):
        obj = self.model(
                    name=name,
                    code=code,
                    order=order,
                    municipality=self.municipality,
                    year=self.year,
                    document=self.document_object
                )
        if self.month:
            obj.month = self.month
        return obj

    def parse_file(self, file_path='files/proracun_apra.xlsx'):
        book = xlrd.open_workbook(file_path)
        sheet = book.sheet_by_index(0)

        nodes = {}
        i=0
        start_time = time.time()
        for row_i in range(sheet.nrows):
            # skip first row
            if i == 0:
                i+=1
                continue

            # get first level data and save it
            row = sheet.row(row_i)
            ppp_id = row[2].value
            ppp_name = row[3].value

            if ppp_id in nodes.keys():
                ppp = nodes[ppp_id]
            else:
                ppp = self.prepare_moodel(
                    name=ppp_name,
                    code=ppp_id,
                    order=i,
                )
                ppp.save()
                i+=1
                nodes[ppp_id] = ppp

            # get second level data and save it
            gpr_id = row[4].value
            gpr_name = row[5].value

            if gpr_id in nodes.keys():
                gpr = nodes[gpr_id]
            else:
                gpr = self.prepare_moodel(
                    name=gpr_name,
                    code=gpr_id,
                    order=i,
                )
                gpr.parent=ppp
                gpr.save()
                i+=1
                nodes[gpr_id] = gpr

            # get third level data and save it, or update amount on existed
            ppr_id = row[6].value
            ppr_name = row[7].value

            amount = row[16].value

            if ppr_id in nodes.keys():
                ppr = nodes[ppr_id]
                #ppr.amount += amount
                #ppr.save()
            else:
                ppr = self.prepare_moodel(
                    name=ppr_name,
                    code=ppr_id,
                    order=i,
                )
                ppr.parent=gpr
                #ppr.amount=amount
                ppr.save()
                i+=1
                nodes[ppr_id] = ppr

            # Do tuki je ok

            pp_id = row[8].value
            pp_name = row[9].value
            ppr_pp_id = f'{ppr_id}_{pp_id}'

            if ppr_pp_id in nodes.keys():
                pp = nodes[ppr_pp_id]
            else:
                pp = self.prepare_moodel(
                    name=pp_name,
                    code=pp_id,
                    order=i,
                )
                pp.parent=ppr
                pp.save()
                i+=1
                nodes[ppr_pp_id] = pp

            k4_id = row[10].value
            k4_name = row[11].value
            amount = row[16].value
            ppr_pp_k4_id = f'{ppr_pp_id}_{k4_id}'

            if ppr_pp_k4_id in nodes.keys():
                k4 = nodes[ppr_pp_k4_id]
            else:
                k4 = self.prepare_moodel(
                    name=k4_name,
                    code=k4_id,
                    order=i,
                )

                k4.parent=pp
                k4.amount=amount
                k4.save()
                i+=1
                nodes[k4_id] = k4

        for budget_item in self.model.objects.filter(document=self.document_object, level=3, amount=None):
            budget_item.amount = sum([item.amount for item in budget_item.get_children()])
            budget_item.save()

        for budget_item in self.model.objects.filter(document=self.document_object, level=2, amount=None):
            budget_item.amount = sum([item.amount for item in budget_item.get_children()])
            budget_item.save()

        for budget_item in self.model.objects.filter(document=self.document_object, level=1, amount=None):
            budget_item.amount = sum([item.amount for item in budget_item.get_children()])
            budget_item.save()

        for budget_item in self.model.objects.filter(document=self.document_object, level=0, amount=None):
            budget_item.amount = sum([item.amount for item in budget_item.get_children()])
            budget_item.save()

        print("--- %s seconds ---" % (time.time() - start_time))


class XLSXAppraRevenue(object):
    def __init__(self, document, model, definiton_model, month=None):
        self.municipality = document.municipality
        self.year = document.year
        self.model = model
        self.document_object = document
        self.month = month
        self.definiton_model = definiton_model
        definitons_qeryset = definiton_model.objects.all()
        self.definitons = {d.code: d for d in definitons_qeryset}


    def prepare_moodel(self, name, code,amount):
        obj = self.model(
                    name=name,
                    code=code,
                    municipality=self.municipality,
                    year=self.year,
                    document=self.document_object,
                    definition=self.definitons.get(code, None),
                    amount=amount,
                )
        if self.month:
            obj.month = self.month
        return obj

    def parse_file(self, file_path='files/proracun_apra.xlsx'):
        book = xlrd.open_workbook(file_path)
        sheet = book.sheet_by_index(0)

        nodes = {}
        i=0
        for row_i in range(sheet.nrows):
            # skip first row
            if i == 0:
                i+=1
                continue

            # get first level data and save it
            row = sheet.row(row_i)
            k6_id = row[1].value
            k6_name = row[2].value
            k6_amount = row[3].value

            print(k6_id, k6_name, k6_amount)

            k6 = self.prepare_moodel(
                name=k6_name,
                code=k6_id,
                amount=k6_amount
            )
            k6.save()

# class XLSParser(object):
#     def __init__(self):
#         self.depths = {}
#         self.org = Municipality.objects.get(id=1)
#         self.year = FinancialYear.objects.first()
#         self.parse_file()

#     def parse_line(self, line):
#         return [(i, item) for i, item in enumerate(line) if item]

#     def get_parent_node(self, depth, last_added):
#         current = last_added
#         while self.depths[current.id] >= depth:
#             current = current.parent
#             if not current:
#                 return None
#         return current


#     def parse_file(self, file_path='files/prihodki_ajdovscina_2022.xls'):
#         book = xlrd.open_workbook(file_path)
#         sheet = book.sheet_by_index(0)

#         rows = []
#         for row_i in range(sheet.nrows):
#             row_values = []
#             for cell in sheet.row(row_i):
#                 row_values.append(cell.value)
#             rows.append(row_values)

#         parent = None

#         last_added = None

#         i = 0
#         for row in rows:
#             items = self.parse_line(row)
#             if len(items) != 3:
#                 continue
#             print(items)
#             if last_added:
#                 parent = self.get_parent_node(items[0][0], last_added)
#             else:
#                 parent = None

#             rc = RevenueObcine(
#                 name=items[1][1],
#                 amount=items[2][1],
#                 code=items[0][1],
#                 parent=parent,
#                 order=i,
#                 organization=self.org,
#                 year=self.year)
#             rc.save()
#             self.depths[rc.id] = int(items[0][0])
#             last_added = rc
#             i+=1



class XLSCodesParser(object):
    def __init__(self, model):
        self.depths = {}
        self.model = model
        self.parse_file()


    def parse_line(self, line):
        return [(i, item) for i, item in enumerate(line) if item]

    def get_parent_node(self, depth, last_added):
        current = last_added
        while self.depths[current.id] >= depth:
            current = current.parent
            if not current:
                return None
        return current


    def parse_file(self, file_path='files/kode_matic.xlsx'):
        book = xlrd.open_workbook(file_path)
        sheet = book.sheet_by_index(2)

        rows = []
        for row_i in range(sheet.nrows):
            row_values = []
            for cell in sheet.row(row_i):
                row_values.append(cell.value)
            rows.append(row_values)

        parent = None

        last_added = None

        i = 0
        for row in rows:
            items = self.parse_line(row)
            if len(items) != 2:
                continue
            print(items)
            if last_added:
                parent = self.get_parent_node(items[0][0], last_added)
            else:
                parent = None
            print('pre save')
            rc = self.model(
                name=items[1][1],
                code=int(items[0][1]),
                parent=parent,
                order=i)
            rc.save()
            self.depths[rc.id] = int(items[0][0])
            last_added = rc
            i+=1


def download_image(url, name):
        page = requests.get(url)
        file_path = f'media/{name}'
        with open(file_path, 'wb') as f:
            f.write(page.content)
        return file_path
