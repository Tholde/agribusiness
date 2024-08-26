(function () {
  ("use strict");

  var moreMenuWidth = 116;
  var navbarMenuHTML = document.querySelector(".vertical-menu").innerHTML;
  var default_lang = "en"; // set Default Language
  var language = localStorage.getItem("language") ? localStorage.getItem("language") : default_lang;

  function initLanguage() {
    // Set new language
    (language === null) ? setLanguage(default_lang) : setLanguage(language);
    var languages = document.getElementsByClassName("language");
    languages && Array.from(languages).forEach(function (dropdown) {
      dropdown.addEventListener("click", function (event) {
        setLanguage(dropdown.getAttribute("data-lang"));
        if (document.documentElement.getAttribute("data-layout") === "horizontal") {
          updateHorizontalMenus();
        }
        // document.querySelector("#sidebar-menu").classList.add("opacity-0");
      });
    });
  }

  function setLanguage(lang) {
    if (document.getElementById("header-lang-img")) {
      if (lang == "en") {
        document.getElementById("header-lang-img").src = "assets/images/flags/us.svg";
      } else if (lang == "sp") {
        document.getElementById("header-lang-img").src = "assets/images/flags/spain.svg";
      } else if (lang == "gr") {
        document.getElementById("header-lang-img").src = "assets/images/flags/germany.svg";
      } else if (lang == "it") {
        document.getElementById("header-lang-img").src = "assets/images/flags/italy.svg";
      } else if (lang == "ru") {
        document.getElementById("header-lang-img").src = "assets/images/flags/russia.svg";
      }

      localStorage.setItem("language", lang);
      language = localStorage.getItem("language");
      getLanguage();
    }

  }

  // Multi language setting
  function getLanguage() {
    language == null ? setLanguage(default_lang) : false;
    var request = new XMLHttpRequest();
    // Instantiating the request object
    request.open("GET", "assets/lang/" + language + ".json");
    // Defining event listener for readystatechange event
    request.onreadystatechange = function () {
      // Check if the request is compete and was successful
      if (this.readyState === 4 && this.status === 200) {
        var data = JSON.parse(this.responseText);
        Object.keys(data).forEach(function (key) {
          var elements = document.querySelectorAll("[data-key='" + key + "']");
          Array.from(elements).forEach(function (elem) {
            elem.textContent = data[key];
          });
        });
      }
    };
    // Sending the request to the server
    request.send();
  }

  //togle menu 
  var sidebartoggle = document.querySelectorAll("#vertical-menu-btn");
  sidebartoggle.forEach(function (e) {
    e.addEventListener('click', function () {
      if (window.innerWidth >= 992) {
        if (document.documentElement.getAttribute("data-sidebar-size") == "sm") {
          document.documentElement.setAttribute('data-sidebar-size', 'lg')
        } else {
          document.documentElement.setAttribute('data-sidebar-size', 'sm')
        }
      } else if (window.innerWidth <= 991) {
        document.querySelector('#sidebar').classList.toggle("hidden")
        if (!document.querySelector('#sidebar').classList.contains("hidden")) {
          document.querySelector('#backdrop').classList.remove("hidden")
        } else {
          document.querySelector('#backdrop').classList.add("hidden")
        }
        document.documentElement.setAttribute('data-sidebar-size', 'lg');
      } else {
        document.documentElement.setAttribute('data-sidebar-size', 'lg');
      }
    }
    );
  });

  document.getElementById("backdrop").onclick = function () {//do something
    document.querySelector('#backdrop').classList.add("hidden")
    document.querySelector('#sidebar').classList.add("hidden")
  }

  /********* dropdown common js *********/
  var dropdownElem = document.querySelectorAll('.dropdown');
  var dropupElem = document.querySelectorAll('.dropup');
  var dropStartElem = document.querySelectorAll('.dropstart');
  var dropendElem = document.querySelectorAll('.dropend');
  var isShowDropMenu = false;
  var isMenuInside = false;
  // dropdown event
  dropdownEvent(dropdownElem, 'bottom-start');
  // dropup event
  dropdownEvent(dropupElem, 'top-start');
  // dropstart event
  dropdownEvent(dropStartElem, 'left-start');
  // dropend event
  dropdownEvent(dropendElem, 'right-start');

  function dropdownEvent(elem, place) {
    Array.from(elem).forEach(function (item) {
      item.querySelectorAll(".dropdown-toggle").forEach(function (subitem) {
        subitem.addEventListener("click", function (event) {
          subitem.classList.toggle("show");
          var popper = Popper.createPopper(subitem, item.querySelector(".dropdown-menu"), {
            placement: place
          });

          if (subitem.classList.contains("show") != true) {
            item.querySelector(".dropdown-menu").classList.remove("block")
            item.querySelector(".dropdown-menu").classList.add("hidden")
          } else {
            dismissDropdownMenu()
            item.querySelector(".dropdown-menu").classList.add("block")
            item.querySelector(".dropdown-menu").classList.remove("hidden")
            if (item.querySelector(".dropdown-menu").classList.contains("block")) {
              subitem.classList.add("show")
            } else {
              subitem.classList.remove("show")
            }
            event.stopPropagation();
          }
          isMenuInside = false;
        });
      });
    });
  }

  function dismissDropdownMenu() {
    Array.from(document.querySelectorAll(".dropdown-menu")).forEach(function (item) {
      item.classList.remove("block")
      item.classList.add("hidden")
    });
    Array.from(document.querySelectorAll(".dropdown-toggle")).forEach(function (item) {
      item.classList.remove("show")
    });
    isShowDropMenu = false;
  }

  // dropdown form
  Array.from(document.querySelectorAll(".dropdown-menu")).forEach(function (item) {
    if (item.querySelectorAll("form")) {
      Array.from(item.querySelectorAll("form")).forEach(function (subitem) {
        subitem.addEventListener("click", function (event) {
          if (!isShowDropMenu) {
            isShowDropMenu = true;
          }
        })
      });
    }
  });

  // data-tw-auto-close
  Array.from(document.querySelectorAll(".dropdown-toggle")).forEach(function (item) {
    var elem = item.parentElement
    if (item.getAttribute('data-tw-auto-close') == 'outside') {
      elem.querySelector(".dropdown-menu").addEventListener("click", function () {
        if (!isShowDropMenu) {
          isShowDropMenu = true;
        }
      });
    } else if (item.getAttribute('data-tw-auto-close') == 'inside') {
      item.addEventListener("click", function () {
        isShowDropMenu = true;
        isMenuInside = true;
      });
      elem.querySelector(".dropdown-menu").addEventListener("click", function () {
        isShowDropMenu = false;
        isMenuInside = false;
      });
    }
  });

  window.addEventListener('click', function (e) {
    if (!isShowDropMenu && !isMenuInside) {
      dismissDropdownMenu();
    }
    isShowDropMenu = false;
  });


  let triggers = Array.from(document.querySelectorAll('[data-toggle="collapse"]'));

  window.addEventListener('click', (ev) => {
    const elm = ev.target;
    if (triggers.includes(elm)) {
      const selector = elm.getAttribute('data-target');
      collapse(selector, 'toggle');
    }
  }, false);


  const fnmap = {
    'toggle': 'toggle',
    'show': 'add',
    'hide': 'remove'
  };
  const collapse = (selector, cmd) => {
    const targets = Array.from(document.querySelectorAll(selector));
    targets.forEach(target => {
      target.classList[fnmap[cmd]]('show');
    });
  }

  /********* modal common js *********/
  // openModal
  var modalTrigger = document.querySelectorAll('[data-tw-toggle="modal"]');
  var isModalShow = false;
  Array.from(modalTrigger).forEach(function (item) {
    item.addEventListener("click", function () {
      var target = this.getAttribute('data-tw-target').substr(1);
      var modalWindow = document.getElementById(target);

      if (modalWindow.classList.contains("hidden")) {
        modalWindow.classList.remove('hidden');
        document.body.classList.add('overflow-hidden');
      } else {
        modalWindow.classList.add('hidden');
        document.body.classList.remove('overflow-hidden');
      }
      isModalShow = false;

      if (item.getAttribute('data-tw-backdrop') == 'static') {
        isModalShow = true;
      }
    });
  });

  // closeButton
  var closeButton = document.querySelectorAll('[data-tw-dismiss="modal"]');
  Array.from(closeButton).forEach(function (subElem) {
    subElem.addEventListener("click", function () {

      var modalWindow = subElem.closest(".modal");
      if (modalWindow.classList.contains("hidden")) {
        modalWindow.classList.remove('hidden');
        document.body.classList.add('overflow-hidden');
      } else {
        modalWindow.classList.add('hidden');
        document.body.classList.remove('overflow-hidden');
      }
    });
  });


  // closeButton
  var closeButton = document.querySelectorAll('[data-tw-dismiss="toast"]');
  Array.from(closeButton).forEach(function (subElem) {
    subElem.addEventListener("click", function () {

      var toastWindow = subElem.closest(".toast");
      if (toastWindow.classList.contains("hidden")) {
        toastWindow.classList.remove('hidden');
        document.body.classList.add('overflow-hidden');
      } else {
        toastWindow.classList.add('hidden');
        document.body.classList.remove('overflow-hidden');
      }
    });
  });

  // closeModal
  var modalElem = document.querySelectorAll('.modal');
  Array.from(modalElem).forEach(function (elem) {

    // modalOverlay
    var modalOverlay = elem.querySelectorAll('.modal-overlay');
    Array.from(modalOverlay).forEach(function (subItem) {
      subItem.addEventListener("click", function () {
        if (!isModalShow) {
          if (elem.classList.contains("hidden")) {
            elem.classList.remove('hidden');
            document.body.classList.add('overflow-hidden');
          } else {
            elem.classList.add('hidden');
            document.body.classList.remove('overflow-hidden');
          }
        }
      });
    });

    // Escape
    document.addEventListener("keydown", function (event) {
      var key = event.key;
      if (!isModalShow) {
        if (key == "Escape") {
          elem.classList.add('hidden');
          document.body.classList.remove('overflow-hidden');
        }
      }
    });
  });



  // ltr-rtl
  var isChangeMode = document.getElementById("ltr-rtl");
  if (isChangeMode) {
    isChangeMode.addEventListener("click", function (e) {
      var themeMode = document.documentElement.getAttribute("dir");
      if (themeMode == "ltr") {
        document.documentElement.setAttribute("dir", "rtl");
      } else {
        document.documentElement.setAttribute("dir", "ltr");
      }

      swiperDir();
    });
  }

  function drawerSetting() {
    const allDrawerButtons = document.querySelectorAll('[data-drawer-target]');
    const allDrawerCloseButtons = document.querySelectorAll('[data-drawer-close]');
    const allModalButtons = document.querySelectorAll('[data-modal-target]');
    const allModalCloseButtons = document.querySelectorAll('[data-modal-close]');
    const bodyElement = document.body;

    let openDrawerId = null;
    let openModalId = null;
    const backDropOverlay = document.createElement('div');
    backDropOverlay.className = 'fixed inset-0 bg-gray-900/50 z-[1049]  backdrop-overlay hidden';
    backDropOverlay.id = 'myDiv';
    if (allModalButtons.length > 0 || allDrawerButtons.length > 0)
      document.body.appendChild(backDropOverlay);

    // Function to toggle the state of drawers and modals
    function toggleElementState(elementId, show) {
      const element = document.getElementById(elementId);
      if (element) {
        if (!show) {
          element.classList.add('show');
          backDropOverlay.classList.add('hidden');
          setTimeout(() => {
            element.classList.add("hidden");
          }, 350);
        } else {
          element.classList.remove("hidden");
          setTimeout(() => {
            element.classList.remove('show');
            backDropOverlay.classList.remove('hidden');
          }, 200);
        }
        bodyElement.classList.toggle('overflow-hidden', show);
        if (show) {
          openDrawerId = elementId;
          openModalId = elementId;
        } else {
          openDrawerId = null;
          openModalId = null;
        }
      }
    }

    // Attach click event listeners to drawer buttons
    allDrawerButtons.forEach(element => {
      const drawerId = element.getAttribute('data-drawer-target');
      if (drawerId) {
        element.addEventListener('click', function () {
          toggleElementState(drawerId, true);
        });
      }
    });

    // Attach click event listeners to drawer close buttons
    allDrawerCloseButtons.forEach(element => {
      const drawerId = element.getAttribute('data-drawer-close');
      if (drawerId) {
        element.addEventListener('click', function () {
          toggleElementState(drawerId, false);
        });
      }
    });

    // Attach click event listeners to modal buttons
    allModalButtons.forEach(element => {
      const modalId = element.getAttribute('data-modal-target');
      if (modalId) {
        element.addEventListener('click', function () {
          toggleElementState(modalId, true);
        });
      }
    });

    // Attach click event listeners to modal close buttons
    allModalCloseButtons.forEach(element => {
      const modalId = element.getAttribute('data-modal-close');
      if (modalId) {
        element.addEventListener('click', function () {
          toggleElementState(modalId, false);
        });
      }
    });

    // Attach click event listener to backdrop-overlay
    backDropOverlay?.addEventListener('click', function () {
      if (openDrawerId) {
        toggleElementState(openDrawerId, false);
      }
      if (openModalId) {
        toggleElementState(openModalId, false);
      }
    });
  }
  function pluginData() {
    /**
         * flatpickr
         */
    var flatpickrExamples = document.querySelectorAll("[data-provider]");
    Array.from(flatpickrExamples).forEach(function (item) {
      if (item.getAttribute("data-provider") == "flatpickr") {
        var dateData = {};
        var isFlatpickerVal = item.attributes;
        if (isFlatpickerVal["data-date-format"])
          dateData.dateFormat = isFlatpickerVal["data-date-format"].value.toString();
        if (isFlatpickerVal["data-enable-time"]) {
          (dateData.enableTime = true),
            (dateData.dateFormat = isFlatpickerVal["data-date-format"].value.toString() + " H:i");
        }
        if (isFlatpickerVal["data-altFormat"]) {
          (dateData.altInput = true),
            (dateData.altFormat = isFlatpickerVal["data-altFormat"].value.toString());
        }
        if (isFlatpickerVal["data-minDate"]) {
          dateData.minDate = isFlatpickerVal["data-minDate"].value.toString();
          dateData.dateFormat = isFlatpickerVal["data-date-format"].value.toString();
        }
        if (isFlatpickerVal["data-maxDate"]) {
          dateData.maxDate = isFlatpickerVal["data-maxDate"].value.toString();
          dateData.dateFormat = isFlatpickerVal["data-date-format"].value.toString();
        }
        if (isFlatpickerVal["data-default-date"]) {
          dateData.defaultDate = isFlatpickerVal["data-default-date"].value.toString();
          dateData.dateFormat = isFlatpickerVal["data-date-format"].value.toString();
        }
        if (isFlatpickerVal["data-multiple-date"]) {
          dateData.mode = "multiple";
          dateData.dateFormat = isFlatpickerVal["data-date-format"].value.toString();
        }
        if (isFlatpickerVal["data-range-date"]) {
          dateData.mode = "range";
          dateData.dateFormat = isFlatpickerVal["data-date-format"].value.toString();
        }
        if (isFlatpickerVal["data-inline-date"]) {
          (dateData.inline = true),
            (dateData.defaultDate = isFlatpickerVal["data-default-date"].value.toString());
          dateData.dateFormat = isFlatpickerVal["data-date-format"].value.toString();
        }
        if (isFlatpickerVal["data-disable-date"]) {
          var dates = [];
          dates.push(isFlatpickerVal["data-disable-date"].value);
          dateData.disable = dates.toString().split(",");
        }
        if (isFlatpickerVal["data-week-number"]) {
          var dates = [];
          dates.push(isFlatpickerVal["data-week-number"].value);
          dateData.weekNumbers = true
        }
        flatpickr(item, dateData);
      } else if (item.getAttribute("data-provider") == "timepickr") {
        var timeData = {};
        var isTimepickerVal = item.attributes;
        if (isTimepickerVal["data-time-basic"]) {
          (timeData.enableTime = true),
            (timeData.noCalendar = true),
            (timeData.dateFormat = "H:i");
        }
        if (isTimepickerVal["data-time-hrs"]) {
          (timeData.enableTime = true),
            (timeData.noCalendar = true),
            (timeData.dateFormat = "H:i"),
            (timeData.time_24hr = true);
        }
        if (isTimepickerVal["data-min-time"]) {
          (timeData.enableTime = true),
            (timeData.noCalendar = true),
            (timeData.dateFormat = "H:i"),
            (timeData.minTime = isTimepickerVal["data-min-time"].value.toString());
        }
        if (isTimepickerVal["data-max-time"]) {
          (timeData.enableTime = true),
            (timeData.noCalendar = true),
            (timeData.dateFormat = "H:i"),
            (timeData.minTime = isTimepickerVal["data-max-time"].value.toString());
        }
        if (isTimepickerVal["data-default-time"]) {
          (timeData.enableTime = true),
            (timeData.noCalendar = true),
            (timeData.dateFormat = "H:i"),
            (timeData.defaultDate = isTimepickerVal["data-default-time"].value.toString());
        }
        if (isTimepickerVal["data-time-inline"]) {
          (timeData.enableTime = true),
            (timeData.noCalendar = true),
            (timeData.defaultDate = isTimepickerVal["data-time-inline"].value.toString());
          timeData.inline = true;
        }
        flatpickr(item, timeData);
      }
    });
  }

  // menu active
  function initActiveMenu() {

    var menuItems = document.querySelectorAll("#sidebar-menu ul li a");
    menuItems && menuItems.forEach(function (item) {
      var pageUrl = window.location.href.split(/[?#]/)[0];
      if (item.href == pageUrl) {
        item.classList.add("active"); // a- href
        var parent = item.parentElement; // li
        if (parent && parent.id !== "sidebar-menu") {
          parent.classList.add("mm-active"); // li
          var parent2 = parent.parentElement; // ul .
          if (parent2 && parent2.id !== "sidebar-menu") {
            parent2.classList.remove("hidden"); // ul tag
            var parent3 = parent2.parentElement; // li tag
            if (parent3 && parent3.id !== "sidebar-menu") {
              parent3.parentElement.firstElementChild.classList.add("mm-active")
              parent3.parentElement.firstElementChild.firstElementChild.classList.add("has-aerrow");
              var parent4 = parent3.parentElement.parentElement; // ul
              if (parent4 && parent4.id !== "sidebar-menu") {
                parent4.parentElement.parentElement.firstElementChild.classList.add("mm-active")
                if (parent4.parentElement.parentElement.firstElementChild.id !== "sidebar-menu") {
                  parent4.parentElement.parentElement.firstElementChild.firstElementChild.classList.add("has-aerrow");
                  parent4.classList.remove("hidden"); // ul
                }
              }
            }
          }
        }
      }
    });
  }

  // handle sidebar dropdown menu
  function handleSidebarDropdownMenu() {

    var dropdownItem = document.querySelectorAll("#sidebar-menu ul li a.mm-collaps");
    var collasedItem = document.querySelectorAll("#sidebar-menu ul li ul");

    dropdownItem.forEach((item) => {
      item.addEventListener("click", (e) => {
        if (item.parentElement?.nextElementSibling?.children[0]?.classList.contains("hidden")) {
          // remove hidden class from clicked dropdown item
          item.classList.add("has-aerrow");
          item.parentElement.nextElementSibling.children[0].classList.remove("hidden");
          collasedItem.forEach((collapse) => {
            // add hidden class in other rest of dropdown
            if (collapse !== item.parentElement.nextElementSibling.children[0] && !item.classList.contains("child-dropdown")) {
              // remove aerow class
              collapse.parentElement?.previousElementSibling?.firstElementChild?.classList.remove("has-aerrow");
              collapse.classList.add("hidden");
            }
          })
        } else {
          item.classList.remove("has-aerrow");
          item.parentElement?.nextElementSibling?.children[0]?.classList.add("hidden");
        }
      });
    })
  }

  // handle fullscreen icon
  var fullscreenElements = document.querySelector('[data-toggle="fullscreen"]');
  fullscreenElements.addEventListener("click", function () {
    if (document.querySelector(".mid-screen-icon").classList.contains("hidden")) {
      document.querySelector(".full-screen-icon").classList.add("hidden");
      document.querySelector(".mid-screen-icon").classList.remove("hidden");
    } else {
      document.querySelector(".full-screen-icon").classList.remove("hidden");
      document.querySelector(".mid-screen-icon").classList.add("hidden");
    }
  })

  // handle sidebar scroll
  function initMenuItemScroll() {
    setTimeout(function () {
      var sidebarMenu = document.getElementById("sidebar-menu");
      if (sidebarMenu) {
        var currentPath = location.pathname == "/" ? "index.html" : location.pathname.substring(1);
        currentPath = currentPath.substring(currentPath.lastIndexOf("/") + 1);
        var activeMenu = document.getElementById("sidebar-menu").querySelector('[href="' + currentPath + '"]');

        var offset = activeMenu ? activeMenu.offsetTop : 0;
        if (offset > 300) {
          var verticalMenu = document.getElementsByClassName("vertical-menu") ? document.getElementsByClassName("vertical-menu")[0] : "";
          var scrollWrapper = verticalMenu.querySelector(".simplebar-content-wrapper");
          if (verticalMenu && scrollWrapper) {
            setTimeout(function () {
              var scrollTop = offset == 330 ? offset + 85 : offset - 150;
              scrollWrapper.scrollTo({
                top: scrollTop,
                behavior: "smooth"
              })
            }, 0);
          }
        }
      }
    }, 250);
  }

  // set default attribute
  function setDefaultAttribute() {
    if (!sessionStorage.getItem("defaultAttribute")) {
      var attributesValue = document.documentElement.attributes;
      var isLayoutAttributes = {};
      Array.from(attributesValue).forEach(function (x) {
        if (x && x.nodeName && x.nodeName != "undefined") {
          var nodeKey = x.nodeName;
          isLayoutAttributes[nodeKey] = x.nodeValue;
          sessionStorage.setItem(nodeKey, x.nodeValue);
        }
      });
      sessionStorage.setItem("defaultAttribute", JSON.stringify(isLayoutAttributes));
      layoutSwitch(isLayoutAttributes);

      // open right sidebar on first time load
      var offCanvas = document.querySelector('.btn[data-bs-target="#theme-settings-offcanvas"]');
      offCanvas && offCanvas.click();
    } else {
      var isLayoutAttributes = {};
      var attributesToRetrieve = [
        "dir",
        "data-mode",
        "data-layout",
        "data-sidebar",
        "data-sidebar-size",
        "data-topbar",
      ];
      attributesToRetrieve.forEach(function (attribute) {
        isLayoutAttributes[attribute] = sessionStorage.getItem(attribute);

      });
      layoutSwitch(isLayoutAttributes);
    }
  }
  function setAttrItemAndTag(attr, val) {
    document.documentElement.setAttribute(attr, val);
    sessionStorage.setItem(attr, val);
  }
  function removeActiveClass(selector) {
    selector.forEach(function (otherButton) {
      otherButton.classList.remove('active');
    });
  }

  function layoutSetting(isLayout) {
    const sidebarButton = document.querySelectorAll('button[name="data-sidebar-size"]');
    sidebarButton.forEach(function (radioButton) {
      radioButton.addEventListener('click', function () {
        setAttrItemAndTag("data-sidebar-size", this.value);
        removeActiveClass(sidebarButton)
        if (!this.classList.contains('active')) {
          this.classList.add('active')
        } else {
          this.classList.remove('active')
        }

      });
    });

    const layoutButtons = document.querySelectorAll('input[name="data-layout"]');
    layoutButtons.forEach(function (radioButton) {
      radioButton.addEventListener('click', function () {
        setAttrItemAndTag("data-layout", this.value);
        updateRadio(this.id);
        if (this.value == "vertical") {

          document.querySelector(".vertical-menu").innerHTML = navbarMenuHTML
          const NewMetisMenu = new MetisMenu("#sidebar-menu");
          NewMetisMenu.update();
          initActiveMenu();
          getLanguage();
          handleSidebarDropdownMenu();
          document.documentElement.setAttribute("data-sidebar-size","lg")

        } else {
          updateHorizontalMenus()
          getLanguage();
        }

      });
    });

    const layoutradioButtons = document.querySelectorAll('button[name="data-mode"]');
    layoutradioButtons.forEach(function (radioButton) {
      radioButton.addEventListener('click', function () {
        setAttrItemAndTag("data-mode", this.value);
        if (this.value == "dark") {
          setAttrItemAndTag("data-topbar", "dark");
          updateActivebtn("topbar-dark")
          removeActivebtn("topbar-light")
        } else if (document.documentElement.getAttribute("data-layout") == "horizontal") {
          setAttrItemAndTag("data-topbar", "light");
          updateActivebtn("topbar-light")
          removeActivebtn("topbar-dark")
        } else if (this.value == "light") {
          setAttrItemAndTag("data-topbar", "light");
          updateActivebtn("topbar-light")
          removeActivebtn("topbar-dark")
        }
        removeActiveClass(layoutradioButtons)
        if (!this.classList.contains('active')) {
          this.classList.add('active')
        } else {
          this.classList.remove('active')
        }
      });
    });

    const sidebarcolor = document.querySelectorAll('button[name="data-sidebar-color"]');
    sidebarcolor.forEach(function (radioButton) {
      radioButton.addEventListener('click', function () {
        removeActiveClass(sidebarcolor)
        setAttrItemAndTag("data-sidebar", this.value);
        if (!this.classList.contains('active')) {
          this.classList.add('active')
        } else {
          this.classList.remove('active')
        }
      })

    });

    const topbarcolorredio = document.querySelectorAll('button[name="data-topbar"]');
    topbarcolorredio.forEach(function (radioButton) {
      radioButton.addEventListener('click', function () {
        setAttrItemAndTag("data-topbar", this.value);
        removeActiveClass(topbarcolorredio)
        if (!this.classList.contains('active')) {
          this.classList.add('active')
        } else {
          this.classList.remove('active')
        }
      });
    });

    const layoutmodeButtons = document.querySelectorAll('button[name="dir"]');
    layoutmodeButtons.forEach(function (radioButton) {
      radioButton.addEventListener('click', function () {
        setAttrItemAndTag("dir", this.value);
        removeActiveClass(layoutmodeButtons)
        if (!this.classList.contains('active')) {
          this.classList.add('active')
        } else {
          this.classList.remove('active')
        }
      });
    });
  }

  // updateRadio Btn
  function updateRadio(radioId) {
    document.getElementById(radioId).checked = true;
  }
  function updateActivebtn(btnId) {
    document.getElementById(btnId).classList.add("active");
  }
  function removeActivebtn(btnId) {
    document.getElementById(btnId).classList.remove("active");
  }

  // set full layout
  function layoutSwitch(isLayoutAttributes) {
    switch (isLayoutAttributes) {
      case isLayoutAttributes:
        switch (isLayoutAttributes["data-mode"]) {
          case "light":
            setAttrItemAndTag("data-mode", "light");
            updateActivebtn("data-mode-light")
            break;
          case "dark":
            setAttrItemAndTag("data-mode", "dark");
            updateActivebtn("data-mode-dark")
            break;
          default:
            setAttrItemAndTag("data-mode", "light");
            updateActivebtn("data-mode-light")
            break;
        }
        switch (isLayoutAttributes["data-layout"]) {
          case "horizontal":
            setAttrItemAndTag("data-layout", "horizontal");
            updateRadio("horizontal")
            break;
          case "vertical":
            setAttrItemAndTag("data-layout", "vertical");
            updateRadio("vertical")
            break;
          default:
            setAttrItemAndTag("data-layout", "vertical");
            updateRadio("vertical")
            break;
        }
        switch (isLayoutAttributes["data-sidebar"]) {
          case "light":
            setAttrItemAndTag("data-sidebar", "light");
            updateActivebtn("data-sidebar-light");
            break;
          case "dark":
            setAttrItemAndTag("data-sidebar", "dark");
            updateActivebtn("data-sidebar-dark")
            break;
          default:
            setAttrItemAndTag("data-sidebar", "light");
            updateActivebtn("data-sidebar-light")
            break;
        }
        switch (isLayoutAttributes["data-topbar"]) {
          case "light":
            setAttrItemAndTag("data-topbar", "light");
            updateActivebtn("topbar-light")
            break;
          case "dark":
            setAttrItemAndTag("data-topbar", "dark");
            updateActivebtn("topbar-dark")
            break;
          default:
            setAttrItemAndTag("data-topbar", "light");
            updateActivebtn("topbar-light")
            break;
        }
        switch (isLayoutAttributes["data-sidebar-size"]) {
          case "lg":
            setAttrItemAndTag("data-sidebar-size", "lg");
            updateActivebtn("sidebar-size-lg")
            break;
          case "md":
            setAttrItemAndTag("data-sidebar-size", "md");
            updateActivebtn("sidebar-size-md")
            break;
          case "sm":
            setAttrItemAndTag("data-sidebar-size", "sm");
            updateActivebtn("sidebar-size-sm")
            break;
          default:
            setAttrItemAndTag("data-sidebar-size", "lg");
            updateActivebtn("sidebar-size-lg")
            break;
        }
        switch (isLayoutAttributes["data-mode"]) {
          case "light":
            setAttrItemAndTag("data-mode", "light");
            updateActivebtn("data-mode-light")
            break;
          case "dark":
            setAttrItemAndTag("data-mode", "dark");
            updateActivebtn("data-mode-dark")
            break;
          default:
            setAttrItemAndTag("data-mode", "light");
            updateActivebtn("data-mode-light")
            break;
        }
        switch (isLayoutAttributes["dir"]) {
          case "ltr":
            setAttrItemAndTag("dir", "ltr");
            updateActivebtn("data-mode-ltr")
            break;
          case "rtl":
            setAttrItemAndTag("dir", "rtl");
            updateActivebtn("data-mode-rtl")
            break;
          default:
            setAttrItemAndTag("dir", "ltr");
            updateActivebtn("data-mode-ltr")
            break;
        }
      default:
        break;
    }
  }
  // horizontal menus
  function updateHorizontalMenus() {
    
    document.documentElement.removeAttribute("data-sidebar-size")

    const layoutType = sessionStorage.getItem("data-layout")
    const getSidebarSize = sessionStorage.getItem("data-sidebar-size")
    if (layoutType != "horizontal") {
      document.documentElement.setAttribute("data-sidebar-size",getSidebarSize)
      return;
    }

    const navbarMenu = document.querySelector(".vertical-menu");
    if (navbarMenu) {
      navbarMenu.innerHTML = navbarMenuHTML;
    }
    const navbarNav = document.querySelector("#sidebar-menu");
    // count width of horizontal menu
    setTimeout(() => {
      const fullWidthOfMenu = navbarNav.clientWidth - moreMenuWidth - 50;
      const extraMenuName = "More";
      const menuData = document.querySelectorAll(".vertical-menu ul li.nav-items");
      let newMenus = "";
      let splitItem = "";
      let menusWidth = 0;
      Array.prototype.forEach.call(menuData, function (item, index) {
        menusWidth += item.offsetWidth;

        if (menusWidth + 50 > fullWidthOfMenu && fullWidthOfMenu != 0 && window.innerWidth >= 991) {
          newMenus += item.outerHTML
          item.remove();
        } else {
          splitItem = item;
        }
        if (index + 1 === menuData.length) {
          if (splitItem.insertAdjacentHTML && newMenus) {
            splitItem.insertAdjacentHTML("afterend",
              `<li class="nav-items more-link ">
                <div class="group-data-[sidebar-size=sm]:py-4 group-data-[sidebar-size=sm]:px-5 py-3 px-6 flex items-center justify-between text-vertical-menu-item-font-size font-normal transition-all duration-150 ease-linear rounded-sm text-vertical-menu-item active:text-vertical-menu active:bg-vertical-menu-item-bg-active group-data-[sidebar=dark]:text-vertical-menu-item-dark group-data-[sidebar=dark]:hover:text-vertical-menu group-data-[sidebar=dark]:hover:bg-vertical-menu-item-bg-hover-dark group-data-[sidebar=dark]:active:text-vertical-menu group-data-[sidebar=dark]:active:bg-vertical-menu-item-bg-active-dark group-data-[sidebar-size=md]:block group-data-[sidebar-size=sm]:my-0 group-data-[sidebar-size=sm]:rounded-b-none group-data-[layout=horizontal]:m-0 before:content-['\f0140'] before:font-material ltr:before:right-6 rtl:before:left-6 before:text-16 before:absolute relative group-data-[sidebar-size=md]:before:hidden ">
                    <a href="#!" class="mm-collaps group-data-[sidebar-size=lg]:flex flex items-center group-data-[sidebar-size=lg]:items-center">
                        <i class="ltr:mr-2 rtl:ml-2 bx bx-task inline-block text-start text-xl group-data-[sidebar-size=md]:block group-data-[sidebar-size=md]:text-center"></i> <span class="group-data-[sidebar-size=sm]:pl-10 group-data-[sidebar-size=md]:block group-data-[sidebar-size=md]:mt-2 group-data-[sidebar-size=md]:text-center group-data-[sidebar-size=lg]:ltr:pl-4 group-data-[sidebar-size=lg]:rtl:pr-4 whitespace-nowrap" data-key="t-invoices">${extraMenuName}</span>
                    </a>
                </div>
                <div class="sub-navmenu group-data-[sidebar-size=sm]:left-vertical-menu-sm group-data-[sidebar-size=sm]:absolute group-data-[sidebar-size=sm]:rounded-b-sm bg-vertical-menu group-data-[sidebar=dark]:bg-vertical-menu-dark group-data-[sidebar=brand]:bg-vertical-menu-brand group-data-[layout=horizontal]:absolute group-data-[layout=horizontal]:top-full group-data-[layout=horizontal]:w-52 group-data-[layout=horizontal]:rounded-b-md drop-shadow-4xl">
                    <ul class="group-data-[sidebar-size=md]:pl-0 group-data-[sidebar-size=sm]:p-0 group-data-[sidebar-size=sm]:py-2  hidden">
                        ${newMenus}
                    </ul>
                </div>
              </li>`
            )
          }
        }
      });
    }, 50);

    menuPosSetOnClickNHover();
    initActiveMenu();
    handleSidebarDropdownMenu();
    if (window.innerWidth < 991 && sessionStorage.getItem("data-layout") == "horizontal") {
      document.querySelector("#sidebar-menu ul").classList.remove("group-data-[layout=horizontal]:flex");
    }
    setTimeout(() => {
      navbarNav.classList.remove("opacity-0")
    }, 100);
  }

  function menuPosSetOnClickNHover() {
    // more-link
    const isElement = document.querySelectorAll(".metismenu  > li.relative");
    Array.from(isElement).forEach(function (item) {
      item.addEventListener("click", menuItem.bind(this), false);
      item.addEventListener("mouseover", menuItem.bind(this), false);
    });
  }
  // menu item range outside the window
  function menuItem(e) {
    // get the dropdown menu element
    var dropdownMenu = e.target;
    const subMenus = (dropdownMenu.nextElementSibling) ? dropdownMenu.nextElementSibling : dropdownMenu.parentElement.nextElementSibling;
    if (dropdownMenu && subMenus) {
      // get the position and dimensions of the dropdown menu
      var dropdownOffset = subMenus.getBoundingClientRect();
      var dropdownWidth = subMenus.offsetWidth;
      var dropdownHeight = subMenus.offsetHeight;

      // get the dimensions of the screen
      var screenWidth = window.innerWidth;
      var screenHeight = window.innerHeight;

      // calculate the maximum x and y coordinates of the dropdown menu
      var maxDropdownX = dropdownOffset.left + dropdownWidth;
      var maxDropdownY = dropdownOffset.top + dropdownHeight;

      // check if the dropdown menu goes outside the screen
      var isDropdownOffScreen = (maxDropdownX > screenWidth) || (maxDropdownY > screenHeight);
      // if (isDropdownOffScreen) {
      if (subMenus.classList.contains("dropdown-content")) {
        subMenus.classList.add("dropdown-custom-right");
      }
    }

  }
  window.onresize = function () {
    if (sessionStorage.getItem("data-layout") == "horizontal") {
      updateHorizontalMenus();
      getLanguage();
    }
    if (window.innerWidth < 991 && sessionStorage.getItem("data-layout") == "horizontal") {
      document.querySelector("#sidebar-menu ul").classList.remove("group-data-[layout=horizontal]:flex");
    }
  };
  // init fullscreen
  function initFullScreen() {
    $('[data-toggle="fullscreen"]').on("click", function (e) {
      e.preventDefault();
      $('body').toggleClass('fullscreen-enable');
      if (!document.fullscreenElement && /* alternative standard method */ !document.mozFullScreenElement && !document.webkitFullscreenElement) {  // current working methods
        if (document.documentElement.requestFullscreen) {
          document.documentElement.requestFullscreen();
        } else if (document.documentElement.mozRequestFullScreen) {
          document.documentElement.mozRequestFullScreen();
        } else if (document.documentElement.webkitRequestFullscreen) {
          document.documentElement.webkitRequestFullscreen(Element.ALLOW_KEYBOARD_INPUT);
        }
      } else {
        if (document.cancelFullScreen) {
          document.cancelFullScreen();
        } else if (document.mozCancelFullScreen) {
          document.mozCancelFullScreen();
        } else if (document.webkitCancelFullScreen) {
          document.webkitCancelFullScreen();
        }
      }
    });
    document.addEventListener('fullscreenchange', exitHandler);
    document.addEventListener("webkitfullscreenchange", exitHandler);
    document.addEventListener("mozfullscreenchange", exitHandler);
    function exitHandler() {
      if (!document.webkitIsFullScreen && !document.mozFullScreen && !document.msFullscreenElement) {
        $('body').removeClass('fullscreen-enable');
      }
    }
  }
  function init() {
    drawerSetting();
    pluginData();
    initLanguage();
    initActiveMenu();
    initMenuItemScroll();
    setDefaultAttribute();
    updateHorizontalMenus();
    initFullScreen();
    layoutSetting();
  }

  if(sessionStorage.getItem("data-layout") == "vertical") {
    setTimeout(() => {
      handleSidebarDropdownMenu();
    }, 100);
  }

  init();
})();
