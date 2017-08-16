from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category, Base, Item, User

engine = create_engine('sqlite:///itemcatalogwithusers.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Create dummy user
user1 = User(name="Fang Cao", email="fang@google.com",
             picture='https://ichef.bbci.co.uk/news/976/media/images/83351000/jpg/_83351965_explorer273lincolnshirewoldssouthpicturebynicholassilkstone.jpg')
session.add(user1)
session.commit()


category1 = Category(name="Soccer")

session.add(category1)
session.commit()

item1 = Item(user_id=1, name="item1", description="this item's description here", category=category1)

session.add(item1)
session.commit()


item2 = Item(user_id=1, name="item2", description="this item's description here", category=category1)

session.add(item2)
session.commit()

item3 = Item(user_id=1, name="item3", description="this item's description here", category=category1)

session.add(item3)
session.commit()

item4 = Item(user_id=1, name="item4", description="this item's description here", category=category1)

session.add(item4)
session.commit()

item5 = Item(user_id=1, name="item5", description="this item's description here", category=category1)

session.add(item5)
session.commit()

item6= Item(user_id=1, name="item6", description="this item's description here", category=category1)

session.add(item6)
session.commit()

item7 = Item(user_id=1, name="item7", description="this item's description here", category=category1)

session.add(item7)
session.commit()

item8 = Item(user_id=1, name="item8", description="this item's description here", category=category1)

session.add(item8)
session.commit()

item9 = Item(user_id=1, name="item9", description="this item's description here", category=category1)

session.add(item9)
session.commit()


category2 = Category(name="Basketball")

session.add(category2)
session.commit()


item10 = Item(user_id=1, name="item10", description="this item's description here", category=category2)

session.add(item10)
session.commit()

item11 = Item(user_id=1, name="item11", description="this item's description here", category=category2)

session.add(item11)
session.commit()

item12 = Item(user_id=1, name="item12", description="this item's description here", category=category2)

session.add(item12)
session.commit()

item13 = Item(user_id=1, name="item13", description="this item's description here", category=category2)

session.add(item13)
session.commit()

item14 = Item(user_id=1, name="item14", description="this item's description here", category=category2)

session.add(item14)
session.commit()

item15 = Item(user_id=1, name="item15", description="this item's description here", category=category2)

session.add(item15)
session.commit()



category3 = Category(name="Baseball")

session.add(category3)
session.commit()


item16 = Item(user_id=1, name="item16", description="this item's description here", category=category3)

session.add(item16)
session.commit()

item17 = Item(user_id=1, name="item17", description="this item's description here", category=category3)

session.add(item17)
session.commit()

item18 = Item(user_id=1, name="item18", description="this item's description here", category=category3)

session.add(item18)
session.commit()

item19 = Item(user_id=1, name="item19", description="this item's description here", category=category3)

session.add(item19)
session.commit()

item20 = Item(user_id=1, name="item20", description="this item's description here", category=category3)

session.add(item20)
session.commit()


category4 = Category(name="Frisbee")

session.add(category4)
session.commit()


item21 = Item(user_id=1, name="item21", description="this item's description here", category=category4)

session.add(item21)
session.commit()

item22 = Item(user_id=1, name="item22", description="this item's description here", category=category4)

session.add(item22)
session.commit()

item23 = Item(user_id=1, name="item23", description="this item's description here", category=category4)

session.add(item23)
session.commit()

item24 = Item(user_id=1, name="item24", description="this item's description here", category=category4)

session.add(item24)
session.commit()

item25 = Item(user_id=1, name="item25", description="this item's description here", category=category4)

session.add(item25)
session.commit()

item26 = Item(user_id=1, name="item26", description="this item's description here", category=category4)

session.add(item26)
session.commit()



category5 = Category(name="Snowboarding")

session.add(category5)
session.commit()


item27 = Item(user_id=1, name="item27", description="this item's description here", category=category5)

session.add(item27)
session.commit()

item28 = Item(user_id=1, name="item28", description="this item's description here", category=category5)

session.add(item28)
session.commit()

item29 = Item(user_id=1, name="item29", description="this item's description here", category=category5)

session.add(item29)
session.commit()

item30 = Item(user_id=1, name="item30", description="this item's description here", category=category5)

session.add(item30)
session.commit()

item31 = Item(user_id=1, name="item31", description="this item's description here", category=category5)

session.add(item31)
session.commit()


category6 = Category(name="Rock Climbing")

session.add(category6)
session.commit()


item32 = Item(user_id=1, name="item32", description="this item's description here", category=category6)

session.add(item32)
session.commit()


item33 = Item(user_id=1, name="item33", description="this item's description here", category=category6)

session.add(item33)
session.commit()


item34 = Item(user_id=1, name="item34", description="this item's description here", category=category6)

session.add(item34)
session.commit()


item35 = Item(user_id=1, name="item35", description="this item's description here", category=category6)

session.add(item35)
session.commit()

item36 = Item(user_id=1, name="item36", description="this item's description here", category=category6)

session.add(item36)
session.commit()


category7 = Category(name="Foosball")

session.add(category7)
session.commit()

item37 = Item(user_id=1, name="item37", description="this item's description here", category=category7)

session.add(item37)
session.commit()


item38 = Item(user_id=1, name="item38", description="this item's description here", category=category7)

session.add(item38)
session.commit()


item39 = Item(user_id=1, name="item39", description="this item's description here", category=category7)

session.add(item39)
session.commit()


item40 = Item(user_id=1, name="item40", description="this item's description here", category=category7)

session.add(item40)
session.commit()

item41 = Item(user_id=1, name="item41", description="this item's description here", category=category7)

session.add(item41)
session.commit()

item42 = Item(user_id=1, name="item42", description="this item's description here", category=category7)

session.add(item42)
session.commit()

item43 = Item(user_id=1, name="item43", description="this item's description here", category=category7)

session.add(item43)
session.commit()



category8 = Category(name="Skating")

session.add(category8)
session.commit()



item44 = Item(user_id=1, name="item44", description="this item's description here", category=category8)

session.add(item44)
session.commit()

item45 = Item(user_id=1, name="item45", description="this item's description here", category=category8)

session.add(item45)
session.commit()


item46 = Item(user_id=1, name="item46", description="this item's description here", category=category8)

session.add(item46)
session.commit()


category9 = Category(name="Hockey")

session.add(category9)
session.commit()


item47 = Item(user_id=1, name="item47", description="this item's description here", category=category9)

session.add(item47)
session.commit()

item48 = Item(user_id=1, name="item48", description="this item's description here", category=category9)

session.add(item48)
session.commit()


item49 = Item(user_id=1, name="item49", description="this item's description here", category=category9)

session.add(item49)
session.commit()


print "added menu items!"