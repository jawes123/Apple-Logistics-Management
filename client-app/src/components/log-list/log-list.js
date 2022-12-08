import React from "react";
import Card from "../card/card"
import Typography from '@material-ui/core/Typography';
import { Item } from './log-list.styles';

const LogList = ({items, type}) => {
    const roleView = (item) => {
        switch (type.toLowerCase()){
            case "manager": 
                return(
                    <div>
                        <Typography variant="h5" component="h2">Name: {item.username}</Typography>
                        <Typography color="yellow">Product ID: {item.product_id}</Typography>
                        <Typography >Date Created: {item.date_created}</Typography>
                        <Typography >Location: {item.location_id}</Typography>
                    </div>
                )
            case "recipient":
                return(
                    <div>
                        <Typography variant="h5" component="h2">Name: {item.username}</Typography>
                        <Typography color="yellow">Product ID: {item.product_id}</Typography>
                        <Typography >Date Created: {item.date_created}</Typography>
                    </div>
                )
            case "shipper":
                return(
                    <div>
                        <Typography variant="h5" component="h2">Location: {item.location_id}</Typography>
                        <Typography color="yellow">Product ID:{item.product_id}</Typography>
                        <Typography >Date Created: {item.date_created}</Typography>
                    </div>
                )
         }
    }
    
    return (
        <Item>
            {
                items.map(item => (
                    <Card info={roleView(item)} />
                ))
            }
        </Item>
    )
}

export default LogList;