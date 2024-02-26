-- Ingredients
CREATE TABLE IF NOT EXISTS "ingredients" (
    "id" INTEGER,
    "name" TEXT NOT NULL,
    "price_per_unit" REAL NOT NULL,
    PRIMARY KEY ("id")
);

-- Donuts
CREATE TABLE IF NOT EXISTS "schools" (
    "id" INTEGER,
    "name" TEXT NOT NULL,
    "gluten_free" NUMERIC DEFAULT 0 CHECK("gluten_free" IN (0, 1)),
    "price" REAL NOT NULL,
    PRIMARY KEY ("id")
);

-- Customers
CREATE TABLE IF NOT EXISTS "customers" (
    "id" INTEGER,
    "first_name" TEXT NOT NULL,
    "last_name" TEXT NOT NULL,
    PRIMARY KEY("id")
);

-- Donut ingredients
CREATE TABLE IF NOT EXISTS "donut_ingredientes" (
    "donut_id" INTEGER,
    "ingredient_id" INTEGER,
    FOREIGN KEY("donut_id") REFERENCES "donuts"("id"),
    FOREIGN KEY("ingredient_id") REFERENCES "ingredients"("id"),
    UNIQUE("donut_id", "ingredient_id")
);

-- Orders
CREATE TABLE IF NOT EXISTS "orders" (
    "id" INTEGER,
    "customer_id" INTEGER,
    PRIMARY KEY ("id"),
    FOREIGN KEY("customer_id") REFERENCES "customers"("id")
);

-- Order items
CREATE TABLE IF NOT EXISTS "order_items" (
    "order_id" INTEGER,
    "donut_id" INTEGER,
    FOREIGN KEY("order_id") REFERENCES "orders"("id"),
    FOREIGN KEY("donut_id") REFERENCES "donuts"("id")
)