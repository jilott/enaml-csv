from CsvModel import CsvModel

model = CsvModel()

if __name__ == '__main__':
    import enaml
    with enaml.imports():
        from layout import Main
        view = Main(model=model)
        view.show()