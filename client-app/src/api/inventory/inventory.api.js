import axios from "axios";
import { websitePrefix } from "../api.constants";

export const addInventory = (category_id, model, color, size, release) => {
    const form = new FormData();
    form.append("category_id", category_id);
    form.append("model", model);
    form.append("color", color);
    form.append("size", size);
    form.append("release", release);
    return axios({
        url: websitePrefix + "api/inventory/add",
        data: form,
        method: "POST",
        headers: { "Content-Type": "multipart/form-data" },
        mode: "cors",
      });
}

export const getInventory = () => {
    return axios({
        url: websitePrefix + "api/inventory/products",
        method: "GET",
        headers: { "Content-Type": "application/json" },
        mode: "cors",
    })
}
