import React, {useState} from "react";
import logo from "../../assets/logo.png";
import Button from "../../components/button/button";
import Input from "../../components/input/input";
import LogList from "../../components/log-list/log-list";
import {checkLogs} from "../../api/logs/logs.api";
import {LogContainer, Logo, ButtonStyle} from "./logs.styles";

const Logs = () => {
    const [key, setKey] = useState("");
    const [logs, setLogs] = useState([]);

    const onKeyChange = (e) => {
        setKey(e.target.value)
    }

    const onRequest = () => {
        checkLogs(key).then(
            (response) => {
                setLogs(response.data);
            }
        ).catch((error) => 
            {alert("Incorrect key");}
        );
    }

    return(
        <LogContainer>
            <Logo src={logo} alt="Apple" />
            <p>Enter Key</p>
            <Input
                name="key"
                type="password"
                label="Key"
                value={key}
                inputChange={onKeyChange}
            />
            <ButtonStyle>
                <Button onClick={onRequest} label="Request" />
            </ButtonStyle>
            <p>All Entries:</p>
            <LogList items={logs} type={key}/>
        </LogContainer>
    )
}

export default Logs;