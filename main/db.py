from __future__ import annotations
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
from bson import ObjectId
from pymongo import MongoClient, ReturnDocument, errors
from pymongo.database import Database
from pymongo.collection import Collection

def now_utc() -> datetime:
    return datetime.now(timezone.utc)

def as_oid(value: Any) -> ObjectId:
    if isinstance(value, ObjectId):
        return value
    return ObjectId(str(value))

class Db:
    print("db")
    # def __init__(self, uri: str = "mongodb://localhost:27017", db_name: str = "vending"):
    #     self.uri = uri
    #     self.db_name = db_name
    #     self.client: Optional[MongoClient] = None
    #     self.db: Optional[Database] = None
    #     self.drinks: Optional[Collection] = None
    #     self.users: Optional[Collection] = None
    #     self.roles: Optional[Collection] = None
    #     self.transactions: Optional[Collection] = None
    #     self.stock_items: Optional[Collection] = None
    #
    # def connect(self) -> bool:
    #     try:
    #         self.client = MongoClient(self.uri, serverSelectionTimeoutMS=3000)
    #         self.client.admin.command("ping")
    #         self.db = self.client[self.db_name]
    #         self.drinks = self.db["Drinks"]
    #         self.users = self.db["User"]
    #         self.roles = self.db["Roles"]
    #         self.transactions = self.db["Transactions"]
    #         self.stock_items = self.db["StockItems"]
    #         self._ensure_indexes()
    #         return True
    #     except errors.ServerSelectionTimeoutError:
    #         self.client = None
    #         self.db = None
    #         return False
    #     except Exception:
    #         self.client = None
    #         self.db = None
    #         return False
    #     finally:
    #         pass
    #
    # def close(self) -> None:
    #     if self.client:
    #         self.client.close()
    #         self.client = None
    #         self.db = None
    #
    # def _ensure_indexes(self) -> None:
    #     self.drinks.create_index("key", unique=True, name="ux_key")
    #     self.drinks.create_index("name", name="ix_name")
    #     self.roles.create_index("name", unique=True, name="ux_name")
    #     self.users.create_index("username", unique=True, name="ux_username")
    #     self.users.create_index("email", unique=True, name="ux_email")
    #     self.users.create_index("role_ids", name="ix_role_ids")
    #     self.transactions.create_index([("user_id", 1), ("created_at", -1)], name="ix_user_time")
    #     self.transactions.create_index("drink_id", name="ix_drink_id")
    #     self.transactions.create_index("created_at", name="ix_created_at")
    #     self.stock_items.create_index("drink_id", unique=True, name="ux_drink_id")
    #     self.stock_items.create_index("stock", name="ix_stock")
    #
    # def create_drink(self, *, key: str, name: str, price_cents: int) -> Dict[str, Any]:
    #     doc = {"key": key, "name": name, "price_cents": int(price_cents)}
    #     res = self.drinks.insert_one(doc)
    #     doc["_id"] = res.inserted_id
    #     return doc
    #
    # def get_drink_by_id(self, drink_id: Any) -> Optional[Dict[str, Any]]:
    #     return self.drinks.find_one({"_id": as_oid(drink_id)})
    #
    # def get_drink_by_key(self, key: str) -> Optional[Dict[str, Any]]:
    #     return self.drinks.find_one({"key": key})
    #
    # def list_drinks(self, *, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
    #     return list(self.drinks.find({}).skip(skip).limit(limit))
    #
    # def update_drink(self, drink_id: Any, **changes: Any) -> Optional[Dict[str, Any]]:
    #     allowed = {k: v for k, v in changes.items() if k in {"key", "name", "price_cents"}}
    #     if "price_cents" in allowed:
    #         allowed["price_cents"] = int(allowed["price_cents"])
    #     if not allowed:
    #         return self.get_drink_by_id(drink_id)
    #     return self.drinks.find_one_and_update(
    #         {"_id": as_oid(drink_id)},
    #         {"$set": allowed},
    #         return_document=ReturnDocument.AFTER,
    #     )
    #
    # def delete_drink(self, drink_id: Any) -> bool:
    #     return self.drinks.delete_one({"_id": as_oid(drink_id)}).deleted_count == 1
    #
    # def create_role(self, *, name: str, permissions: List[str]) -> Dict[str, Any]:
    #     doc = {"name": name, "permissions": list(permissions)}
    #     res = self.roles.insert_one(doc)
    #     doc["_id"] = res.inserted_id
    #     return doc
    #
    # def get_role_by_id(self, role_id: Any) -> Optional[Dict[str, Any]]:
    #     return self.roles.find_one({"_id": as_oid(role_id)})
    #
    # def get_role_by_name(self, name: str) -> Optional[Dict[str, Any]]:
    #     return self.roles.find_one({"name": name})
    #
    # def list_roles(self, *, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
    #     return list(self.roles.find({}).skip(skip).limit(limit))
    #
    # def update_role(self, role_id: Any, **changes: Any) -> Optional[Dict[str, Any]]:
    #     allowed = {k: v for k, v in changes.items() if k in {"name", "permissions"}}
    #     if not allowed:
    #         return self.get_role_by_id(role_id)
    #     return self.roles.find_one_and_update(
    #         {"_id": as_oid(role_id)},
    #         {"$set": allowed},
    #         return_document=ReturnDocument.AFTER,
    #     )
    #
    # def delete_role(self, role_id: Any) -> bool:
    #     return self.roles.delete_one({"_id": as_oid(role_id)}).deleted_count == 1
    #
    # def create_user(
    #         self,
    #         *,
    #         username: str,
    #         email: str,
    #         role_ids: Optional[List[Any]] = None,
    #         balance_cents: int = 0,
    #         is_active: bool = True,
    #         created_at: Optional[datetime] = None,
    # ) -> Dict[str, Any]:
    #     doc = {
    #         "username": username,
    #         "email": email,
    #         "role_ids": [as_oid(x) for x in (role_ids or [])],
    #         "balance_cents": int(balance_cents),
    #         "is_active": bool(is_active),
    #         "created_at": created_at or now_utc(),
    #     }
    #     res = self.users.insert_one(doc)
    #     doc["_id"] = res.inserted_id
    #     return doc
    #
    # def get_user_by_id(self, user_id: Any) -> Optional[Dict[str, Any]]:
    #     return self.users.find_one({"_id": as_oid(user_id)})
    #
    # def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
    #     return self.users.find_one({"username": username})
    #
    # def list_users(self, *, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
    #     return list(self.users.find({}).skip(skip).limit(limit))
    #
    # def update_user(self, user_id: Any, **changes: Any) -> Optional[Dict[str, Any]]:
    #     allowed_keys = {"username", "email", "role_ids", "balance_cents", "is_active"}
    #     update: Dict[str, Any] = {k: v for k, v in changes.items() if k in allowed_keys}
    #     if "role_ids" in update:
    #         update["role_ids"] = [as_oid(x) for x in update["role_ids"]]
    #     if "balance_cents" in update:
    #         update["balance_cents"] = int(update["balance_cents"])
    #     if not update:
    #         return self.get_user_by_id(user_id)
    #     return self.users.find_one_and_update(
    #         {"_id": as_oid(user_id)},
    #         {"$set": update},
    #         return_document=ReturnDocument.AFTER,
    #     )
    #
    # def delete_user(self, user_id: Any) -> bool:
    #     return self.users.delete_one({"_id": as_oid(user_id)}).deleted_count == 1
    #
    # def create_transaction(
    #         self,
    #         *,
    #         user_id: Any,
    #         amount_cents: int,
    #         drink_id: Optional[Any] = None,
    #         created_at: Optional[datetime] = None,
    #         meta: Optional[Dict[str, Any]] = None,
    # ) -> Dict[str, Any]:
    #     doc = {
    #         "user_id": as_oid(user_id),
    #         "drink_id": as_oid(drink_id) if drink_id is not None else None,
    #         "amount_cents": int(amount_cents),
    #         "created_at": created_at or now_utc(),
    #         "meta": dict(meta or {}),
    #     }
    #     res = self.transactions.insert_one(doc)
    #     doc["_id"] = res.inserted_id
    #     return doc
    #
    # def get_transaction_by_id(self, tx_id: Any) -> Optional[Dict[str, Any]]:
    #     return self.transactions.find_one({"_id": as_oid(tx_id)})
    #
    # def list_transactions(
    #         self,
    #         *,
    #         user_id: Optional[Any] = None,
    #         drink_id: Optional[Any] = None,
    #         skip: int = 0,
    #         limit: int = 100,
    # ) -> List[Dict[str, Any]]:
    #     q: Dict[str, Any] = {}
    #     if user_id is not None:
    #         q["user_id"] = as_oid(user_id)
    #     if drink_id is not None:
    #         q["drink_id"] = as_oid(drink_id)
    #     cur = self.transactions.find(q).sort("created_at", -1).skip(skip).limit(limit)
    #     return list(cur)
    #
    # def delete_transaction(self, tx_id: Any) -> bool:
    #     return self.transactions.delete_one({"_id": as_oid(tx_id)}).deleted_count == 1
    #
    # def create_stock_item(self, *, drink_id: Any, stock: int) -> Dict[str, Any]:
    #     if self.drinks.count_documents({"_id": as_oid(drink_id)}, limit=1) == 0:
    #         raise ValueError(f"Drink {drink_id} existiert nicht")
    #     doc = {"drink_id": as_oid(drink_id), "stock": int(stock)}
    #     res = self.stock_items.insert_one(doc)
    #     doc["_id"] = res.inserted_id
    #     return doc
    #
    # def get_stock_item_by_id(self, item_id: Any) -> Optional[Dict[str, Any]]:
    #     return self.stock_items.find_one({"_id": as_oid(item_id)})
    #
    # def get_stock_item_by_drink(self, drink_id: Any) -> Optional[Dict[str, Any]]:
    #     return self.stock_items.find_one({"drink_id": as_oid(drink_id)})
    #
    # def list_stock_items(self) -> List[Dict[str, Any]]:
    #     return list(self.stock_items.find({}))
    #
    # def update_stock_item(self, item_id: Any, **changes: Any) -> Optional[Dict[str, Any]]:
    #     allowed = {k: v for k, v in changes.items() if k in {"drink_id", "stock"}}
    #     if "drink_id" in allowed:
    #         allowed["drink_id"] = as_oid(allowed["drink_id"])
    #         if self.drinks.count_documents({"_id": allowed["drink_id"]}, limit=1) == 0:
    #             raise ValueError(f"Drink {allowed['drink_id']} existiert nicht")
    #     if "stock" in allowed:
    #         allowed["stock"] = int(allowed["stock"])
    #     if not allowed:
    #         return self.get_stock_item_by_id(item_id)
    #     return self.stock_items.find_one_and_update(
    #         {"_id": as_oid(item_id)},
    #         {"$set": allowed},
    #         return_document=ReturnDocument.AFTER,
    #     )
    #
    # def delete_stock_item(self, item_id: Any) -> bool:
    #     return self.stock_items.delete_one({"_id": as_oid(item_id)}).deleted_count == 1
    #
    # def increment_stock(self, item_id: Any, delta: int) -> Optional[Dict[str, Any]]:
    #     return self.stock_items.find_one_and_update(
    #         {"_id": as_oid(item_id)},
    #         {"$inc": {"stock": int(delta)}},
    #         return_document=ReturnDocument.AFTER,
    #     )
    #
    # def list_stock_with_drink(self, *, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
    #     pipeline = [
    #         {"$lookup": {
    #             "from": "drinks",
    #             "localField": "drink_id",
    #             "foreignField": "_id",
    #             "as": "drink"
    #         }},
    #         {"$unwind": "$drink"},
    #         {"$skip": skip},
    #         {"$limit": limit},
    #     ]
    #     return list(self.stock_items.aggregate(pipeline))
