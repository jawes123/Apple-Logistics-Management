import React, {useState, useEffect} from "react";
import logo from "../../assets/logo.png";
import Button from "../../components/button/button";
import Input from "../../components/input/input";
import ProductList from "../../components/product-list/product-list";
import {getInventory, addInventory} from "../../api/inventory/inventory.api";
import { InventoryContainer, Logo, ButtonStyle } from "./inventory.styles";

const Inventory = () => {
    const [products, setProducts] = useState([]);
    const [category_id, setCategoryId] = useState("");
    const [model, setModel] = useState("");
    const [color, setColor] = useState("");
    const [size, setSize] = useState(""); 
    const [release, setRelease] = useState("");
    const [update, setUpdate] = useState(true);

    const onCategoryIdChange = (e) => {
        setCategoryId(e.target.value);
    }

    const onModelChange = (e) => {
        setModel(e.target.value);
    }
    
    const onColorChange = (e) => {
        setColor(e.target.value);
    }

    const onSizeChange = (e) => {
        setSize(e.target.value);
    }

    const onReleaseChange = (e) => {
        setRelease(e.target.value);
    }

    const onAddRequest = () => {
        addInventory(category_id, model, color, size, release)
        .then((response) => setUpdate(!update)).catch((error) => {
            alert("Something went wrong, Recorded " + error);
        });
    }

    useEffect( () => {
        getInventory().then(response => {
            setProducts(response.data)
        })
    },[update]);
    
    return(
        <InventoryContainer>
            <Logo src={logo} alt="Apple" />
            <p>All Products</p>
            <ProductList items={products} />
            <p>Add Product</p>
            <Input
                category="category_id"
                type="text"
                label="Category"
                value={category_id}
                inputChange={onCategoryIdChange}
            />
            <Input
                category="model"
                type="text"
                label="Model"
                value={model}
                inputChange={onModelChange}
            />
            <Input
                category="color"
                type="text"
                label="Color"
                value={color}
                inputChange={onColorChange}
            />
            <Input
                category="size"
                type="number"
                label="Size"
                value={size}
                inputChange={onSizeChange}
            />
            <Input
                category="release"
                type="number"
                label="Release"
                value={release}
                inputChange={onReleaseChange}
            />
            <ButtonStyle>
                <Button onClick={onAddRequest} label="Add Product" />
            </ButtonStyle>
        </InventoryContainer>
    )
}

export default Inventory;