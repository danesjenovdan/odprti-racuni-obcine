(function () {
  const hash = window.location.hash.slice(1);
  const [elemName] = hash.split(";");

  const scrollToElem = document.querySelector(`a[name="${elemName}"]`);
  if (scrollToElem) {
    // scrollToElem.scrollIntoView({
    //   behavior: "instant",
    //   block: "start",
    //   inline: "start",
    // });
  }

  const breadcrumbsElem = document.getElementById("js-breadcrumbs-container");
  const tableElem = document.getElementById("js-table-container");
  if (tableElem) {
    tableElem.style.minHeight = "60vh";
    tableElem.addEventListener("click", onTableRowClick, true);
    tableElem.addEventListener("mouseover", onTableMouseOver, true);
    tableElem.addEventListener("mouseleave", onTableMouseLeave, false);
    fetchTable(window.location.search, window.location.hash);
  }

  window.addEventListener("hashchange", onHashChange);

  function onTableRowClick(event) {
    const row = event.target.closest("tbody tr");
    if (row) {
      const link = row.querySelector(".bar-chart-name a");
      if (link) {
        window.location.hash = link.hash;
        return;
      }
    } else {
      const backLink = event.target.closest(".bar-chart-title a");
      if (backLink) {
        window.location.hash = backLink.hash;
        return;
      }
    }
  }

  let lastHoverCode = null;
  function onTableMouseOver(event) {
    const row = event.target.closest("tbody tr");
    if (row) {
      const elem = row.querySelector(".bar-chart-name a, .bar-chart-name span");
      const code = elem ? elem.dataset.code : null;
      if (code && code !== lastHoverCode) {
        lastHoverCode = code;
        window.postMessage({ type: "bar-chart-row-hover", code }, "*");
      }
    }
    const tbody = event.target.closest("tbody");
    if (!tbody) {
      lastHoverCode = null;
      window.postMessage({ type: "bar-chart-row-hover", code: null }, "*");
    }
  }

  function onTableMouseLeave(event) {
    lastHoverCode = null;
    window.postMessage({ type: "bar-chart-row-hover", code: null }, "*");
  }

  function onHashChange(event) {
    fetchTable(window.location.search, window.location.hash);
  }

  const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("is-revealed");
      }
    });
  });

  function fetchTable(searchString, hashString) {
    const url = new URL(window.__BAR_CHART_TABLE_URL__, window.location.origin);
    url.search = searchString;
    let scrollOnLoad = false;

    const [, code] = hashString.slice(1).split(";");
    if (code) {
      url.searchParams.set("code", code);
      scrollOnLoad = true;
    }

    // only show loader if it takes more than 0.5s
    const loaderTimeout = setTimeout(() => {
      document.querySelector(".loader-bg").classList.remove("hidden-bct");
    }, 500);

    const hideLoader = () => {
      clearTimeout(loaderTimeout);
      document.querySelector(".loader-bg").classList.add("hidden-bct");
    };

    return fetch(url)
      .then(
        (res) => {
          hideLoader();
          if (!res.ok) {
            console.error(res);
            return `<div class="alert alert-warning">${res.statusText}</div>`;
          }
          return res.text();
        },
        (error) => {
          hideLoader();
          console.error(error);
          return `<div class="alert alert-danger">${error.message}</div>`;
        }
      )
      .then((text) => {
        const template = document.createElement("template");
        template.innerHTML = text;

        const breadcrumbs = template.content.querySelector(
          ".table-breadcrumbs-container"
        );
        if (breadcrumbs) {
          breadcrumbsElem.innerText = "";
          breadcrumbsElem.appendChild(breadcrumbs);
        }

        const table = template.content.querySelector(".bar-chart-table");
        if (table) {
          tableElem.innerText = "";
          tableElem.appendChild(table);
        }

        if (scrollOnLoad && scrollToElem) {
          // scrollToElem.scrollIntoView({
          //   behavior: "instant",
          //   block: "start",
          //   inline: "start",
          // });
        }
        tableElem.querySelectorAll("tr").forEach((tr) => {
          revealObserver.observe(tr);
        });
      });
  }
})();
