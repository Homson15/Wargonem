
from sqlalchemy import create_engine, MetaData, Column, Integer, String, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

class dataBase:

    baza = create_engine('sqlite:///settings/EQSave.db')

    MD = MetaData()

    BazaModel = declarative_base(metadata=MD)

    class EQSave(BazaModel):
        __tablename__ = 'EQSave'
        id = Column(Integer, primary_key=True)
        name = Column(String(100), nullable=False)
        belongs = Column(String(100))

    BazaModel.metadata.create_all(baza)

    BDSesja = sessionmaker(bind=baza)

    sesja = BDSesja()

    mapper = inspect(EQSave)

    def __init__(self):
        pass

    def save(self, slots):

        self.BazaModel.metadata.create_all(self.baza)

        for each in slots:
            if each.item["image"] != "blank.png":
                self.sesja.add(self.EQSave(name=each.item["id"], belongs=each.belongs))
                #print(f"Dodano: {each.item['id']} , {each.belongs}")

        self.sesja.commit()
        self.sesja.close()

    def getData(self):

        table = []

        for element in self.sesja.query(self.EQSave):
            if not element.name == "":
                table.append([element.name, element.belongs])

        self.sesja.close()

        return table



