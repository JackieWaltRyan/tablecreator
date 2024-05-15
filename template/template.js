function createElement(tag, params = {}, actions = () => {
}) {
    let el = document.createElement(tag);

    for (let name in params) {
        try {
            el.setAttribute(name, params[name]);
        } catch (e) {
            console.log(e);
        }
    }

    actions(el);

    return el;
}

function zoomIn(event) {
    let zoom = document.getElementById("zoom");

    zoom.style.display = "block";
    zoom.style.top = (event.y - (event["srcElement"]["naturalHeight"] / 2)).toString();
    zoom.style.left = (event.x + 50);
    zoom.style.width = event["srcElement"]["naturalWidth"].toString();
    zoom.style.height = event["srcElement"]["naturalHeight"].toString();
    zoom.style.background = ("url(\"" + event["srcElement"]["currentSrc"] + "\")");
}

function zoomOut() {
    let zoom = document.getElementById("zoom");

    zoom.style.background = "none";
    zoom.style.display = "none";
}

let getURL = new URL(location.href);

function createTable(search = (getURL.searchParams.has("search") ? decodeURIComponent(getURL.searchParams.get("search")) : "")) {
    let thead = document.getElementById("thead");
    let tbody = document.getElementById("tbody");
    let loading = document.getElementById("loading");

    if (thead.children.length === 0) {
        let th = createElement("th", {}, (el) => {
            el.innerText = "Номер";
        });

        thead.appendChild(th);

        for (let name in data[1]) {
            let th = createElement("th", {}, (el) => {
                el.innerText = name;
            });

            thead.appendChild(th);
        }
    }

    tbody.innerHTML = "";
    loading.style.display = "flex";

    for (let item in data) {
        if (search) {
            let search_input = document.getElementById("input");

            if (search_input.value !== search) {
                search_input.value = search;
            }

            if (decodeURIComponent(getURL.searchParams.get("search")) !== search) {
                getURL.searchParams.set("search", encodeURIComponent(search));

                history.pushState(null, null, getURL.href);
            }

            let text = item;

            for (let param in data[item]) {
                if (!["Изображение"].includes(param)) {
                    text += data[item][param];
                }
            }

            let result = search.split(",").find((item) => {
                return text.toLowerCase().includes(item.trim().toLowerCase());
            })

            if (!result) {
                continue;
            }
        } else {
            if (getURL.searchParams.has("search")) {
                getURL.searchParams.delete("search");

                history.pushState(null, null, getURL.href);
            }
        }

        let tr = createElement("tr", {}, (el) => {
            let td = createElement("td", {
                class: "copy",
                title: "Скопировать"
            }, (el2) => {
                el2.innerText = item;

                el2.addEventListener("click", () => {
                    navigator.clipboard.writeText(el2.innerText).then(r => r);
                });
            });

            el.appendChild(td);

            for (let param in data[item]) {
                let td = createElement("td", {}, (el3) => {
                    if (["Изображение", "Фон"].includes(param)) {
                        let img = createElement("img", {
                            src: data[item][param][0]
                        }, (el4) => {
                            el4.addEventListener("mousemove", (event) => {
                                zoomIn(event);
                            });

                            el4.addEventListener("mouseout", () => {
                                zoomOut();
                            });
                        });

                        if (data[item][param].length > 1) {
                            let div = createElement("div", {
                                class: "paginator"
                            }, (el5) => {
                                let index = 0;

                                let but1 = createElement("button", {
                                    class: "paginator_button",
                                    title: "Предыдущий"
                                }, (el6) => {
                                    el6.innerText = "<";

                                    el6.addEventListener("click", () => {
                                        index = (index - 1);

                                        if (index < 0) {
                                            index = (data[item][param].length - 1);
                                        }

                                        img.src = data[item][param][index];

                                        span.innerText = ((index + 1) + " из " + data[item][param].length);
                                    });
                                });

                                let span = createElement("span", {}, (el7) => {
                                    el7.innerText = ("1 из " + data[item][param].length);
                                });

                                let but2 = createElement("button", {
                                    class: "paginator_button",
                                    title: "Следующий"
                                }, (el8) => {
                                    el8.innerText = ">";

                                    el8.addEventListener("click", () => {
                                        index = (index + 1);

                                        if (index >= data[item][param].length) {
                                            index = 0;
                                        }

                                        img.src = data[item][param][index];

                                        span.innerText = ((index + 1) + " из " + data[item][param].length);
                                    });
                                });

                                el5.appendChild(but1);
                                el5.appendChild(span);
                                el5.appendChild(but2);
                            });

                            el3.appendChild(div);
                        }

                        el3.appendChild(img);
                    } else if (param === "Страница") {
                        let a = createElement("a", {
                            title: "Открыть"
                        }, (el4) => {
                            el4.href = data[item][param];
                            el4.target = "_blank";
                            el4.textContent = data[item][param];
                        });

                        el3.appendChild(a);
                    } else if (Array.isArray(data[item][param])) {
                        let div = createElement("div", {
                            class: ((param !== "Описание") ? "copy nowrap" : "copy"),
                            title: "Скопировать"
                        }, (el4) => {
                            el4.innerText = data[item][param][0];

                            el4.addEventListener("click", () => {
                                navigator.clipboard.writeText(el4.innerText).then(r => r);
                            });
                        });

                        el3.appendChild(div);

                        if (data[item][param].length > 1) {
                            let div2 = createElement("div", {
                                class: "paginator"
                            }, (el5) => {
                                let index = 0;

                                let but1 = createElement("button", {
                                    class: "paginator_button",
                                    title: "Предыдущий"
                                }, (el6) => {
                                    el6.innerText = "<";

                                    el6.addEventListener("click", () => {
                                        index = (index - 1);

                                        if (index < 0) {
                                            index = (data[item][param].length - 1);
                                        }

                                        div.innerText = data[item][param][index];

                                        span.innerText = ((index + 1) + " из " + data[item][param].length);
                                    });
                                });

                                let span = createElement("span", {}, (el7) => {
                                    el7.innerText = ("1 из " + data[item][param].length);
                                });

                                let but2 = createElement("button", {
                                    class: "paginator_button",
                                    title: "Следующий"
                                }, (el8) => {
                                    el8.innerText = ">";

                                    el8.addEventListener("click", () => {
                                        index = (index + 1);

                                        if (index >= data[item][param].length) {
                                            index = 0;
                                        }

                                        div.innerText = data[item][param][index];

                                        span.innerText = ((index + 1) + " из " + data[item][param].length);
                                    });
                                });

                                el5.appendChild(but1);
                                el5.appendChild(span);
                                el5.appendChild(but2);
                            });

                            el3.appendChild(div2);
                        }
                    } else {
                        let div = createElement("div", {
                            class: ((param !== "Описание") ? "copy nowrap" : "copy"),
                            title: "Скопировать"
                        }, (el4) => {
                            el4.innerText = data[item][param];

                            el4.addEventListener("click", () => {
                                navigator.clipboard.writeText(el4.innerText).then(r => r);
                            });
                        });

                        el3.appendChild(div);
                    }
                });

                el.appendChild(td);
            }
        });

        tbody.appendChild(tr);
        loading.style.display = "none";
    }
}
