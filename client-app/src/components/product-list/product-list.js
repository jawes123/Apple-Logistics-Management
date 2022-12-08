import React from "react";
import Card from "../card/card"
import Typography from '@material-ui/core/Typography';
import { Item } from './product-list.styles';

const ProductList = ({items}) => {
    return (
        <Item>
            {
                items.map(item => (
                    <Card key={item[0]} info={
                        <div>
                            <Typography variant="h5" component="h2">Model: {item[2]}</Typography>
                            <Typography color="yellow">UUID: {item[0]}</Typography>
                            <Typography >Category: {item[1]}</Typography>
                            <Typography >Color: {item[3]}</Typography>
                            <Typography >Size: {item[4]} in</Typography>
                            <Typography >Release: {item[5]}</Typography>
                        </div>
                    } />
                ))
            }
        </Item>
    )
}

export default ProductList;