let getURL = new URL(location.href);
let searchTimeout = null;

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

function createTable() {
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
        if (getURL.searchParams.has("search")) {
            let search = decodeURIComponent(getURL.searchParams.get("search"));

            let search_input = document.getElementById("search");

            if (search_input.value !== search) {
                search_input.value = search;
            }

            let text = item;

            for (let param in data[item]) {
                if (!["Изображение"].includes(param)) {
                    text += data[item][param];
                }
            }

            if (!search.split(",").find((item) => {
                return text.toLowerCase().includes(item.trim().toLowerCase());
            })) {
                continue;
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

function scrollMenu() {
    let scrollRoot = null;
    let scrollIcon = null;

    let scrollOld = 0;

    document.querySelector("body").appendChild(createElement("div", {
        class: "scroll",
    }, (el) => {
        scrollRoot = el;

        el.appendChild(createElement("img", {
            class: "scroll_icon",
            src: "data:image/svg+xml;base64,PHN2ZyB4bWxucz0naHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmcnIGZpbGw9JyNmZmYnIHZpZXdCb3g9JzAgMCA4IDgnPjxwYXRoIGQ9J001LjI1IDBsLTQgNCA0IDQgMS41LTEuNS0yLjUtMi41IDIuNS0yLjUtMS41LTEuNXonLz48L3N2Zz4="
        }, (el2) => {
            scrollIcon = el2;
        }));

        el.addEventListener("click", () => {
            if (scrollY > 0) {
                scrollOld = scrollY;

                scrollTo(scrollX, 0);
            } else {
                scrollTo(scrollX, scrollOld);

                scrollOld = 0;
            }
        });
    }));

    if (scrollY > 0) {
        scrollRoot.style.display = "flex";

        scrollIcon.style.transform = "rotate(90deg)";
    }

    window.addEventListener("scroll", () => {
        if (scrollY > 0) {
            scrollRoot.style.display = "flex";

            scrollIcon.style.transform = "rotate(90deg)";
        } else if ((scrollY === 0) && (scrollOld > 0)) {
            scrollRoot.style.display = "flex";

            scrollIcon.style.transform = "rotate(270deg)";
        } else {
            scrollRoot.style.display = "none";
        }
    });
}

function loadGoogle() {
    let tag = "G-G9Q1847V56";

    document.querySelector("head").appendChild(createElement("script", {
        type: "text/javascript",
        src: ("https://www.googletagmanager.com/gtag/js?id=" + tag)
    }, (el) => {
        el.addEventListener("load", () => {
            window.dataLayer = (window.dataLayer || []);

            function gtag() {
                dataLayer.push(arguments);
            }

            gtag("js", new Date());
            gtag("config", tag);
        });

        el.addEventListener("error", () => {
            setTimeout(() => {
                loadGoogle();
            }, 1000);
        });
    }));
}

function loadEruda() {
    window.getURL = (window.getURL || new URL(location.href));

    if (getURL.searchParams.has("dev")) {
        document.querySelector("head").appendChild(createElement("script", {
            type: "text/javascript",
            src: "https://cdn.jsdelivr.net/npm/eruda@3.0.1/eruda.min.js"
        }, (el) => {
            el.addEventListener("load", () => {
                eruda.init();
            });

            el.addEventListener("error", () => {
                setTimeout(() => {
                    loadEruda();
                }, 1000);
            });
        }));
    }
}

function bindSearch() {
    document.getElementById("search").addEventListener("input", (event) => {
        clearTimeout(searchTimeout);

        searchTimeout = setTimeout(() => {
            if (event["target"]["value"]) {
                getURL.searchParams.set("search", encodeURIComponent(event["target"]["value"]));

                history.pushState(null, null, getURL.href);
            } else {
                if (getURL.searchParams.has("search")) {
                    getURL.searchParams.delete("search");

                    history.pushState(null, null, getURL.href);
                }
            }

            createTable();
        }, 2000);
    });
}

if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", () => {
        scrollMenu();

        loadGoogle();
        loadEruda();

        bindSearch();
        createTable();
    });
} else {
    scrollMenu();

    loadGoogle();
    loadEruda();

    bindSearch();
    createTable();
}
