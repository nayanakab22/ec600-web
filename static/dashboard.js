async function loadDevices() {

    try {

        const response = await fetch("/api/devices");

        const devices = await response.json();

        const dashboard = document.getElementById("dashboard");

        dashboard.innerHTML = "";

        const deviceIds = Object.keys(devices);

        if (deviceIds.length === 0) {

            dashboard.innerHTML =
                "<p>No T-Box data received yet.</p>";

            return;
        }

        deviceIds.forEach(function (tboxId) {

            const data = devices[tboxId];

            createTboxCard(
                dashboard,
                tboxId,
                data
            );

        });

    } catch (error) {

        console.error(
            "Dashboard error:",
            error
        );

    }
}


function createTboxCard(
    dashboard,
    tboxId,
    data
) {

    const battery1 = data.Battery1 || {};
    const battery2 = data.Battery2 || {};

    const card =
        document.createElement("div");

    card.className = "tbox-card";


    // --------------------------------------------------
    // T-BOX HEADER
    // --------------------------------------------------

    const title =
        document.createElement("h2");

    title.innerText =
        "T-Box: " + tboxId;

    card.appendChild(title);


    const version =
        document.createElement("p");

    version.innerText =
        "Software Version: " +
        (data.sv || "-");

    card.appendChild(version);


    // --------------------------------------------------
    // BATTERY 1
    // --------------------------------------------------

    card.appendChild(
        createBatterySection(
            "Battery 1",
            battery1
        )
    );


    // --------------------------------------------------
    // BATTERY 2
    // --------------------------------------------------

    card.appendChild(
        createBatterySection(
            "Battery 2",
            battery2
        )
    );


    // --------------------------------------------------
    // GPS
    // --------------------------------------------------

    if (
        data.Latitude !== undefined ||
        data.Longitude !== undefined
    ) {

        const gps =
            document.createElement("div");

        gps.className =
            "info-section";

        gps.innerHTML = `
            <h3>GPS</h3>

            <div class="info-grid">

                <div>
                    <span>Latitude</span>
                    <strong>${data.Latitude ?? "-"}</strong>
                </div>

                <div>
                    <span>Longitude</span>
                    <strong>${data.Longitude ?? "-"}</strong>
                </div>

            </div>
        `;

        card.appendChild(gps);
    }


    // --------------------------------------------------
    // SERVER TIME
    // --------------------------------------------------

    if (data._server_time) {

        const serverTime =
            document.createElement("p");

        serverTime.className =
            "server-time";

        serverTime.innerText =
            "Server received: " +
            data._server_time;

        card.appendChild(serverTime);
    }


    dashboard.appendChild(card);
}


function createBatterySection(
    name,
    battery
) {

    const section =
        document.createElement("div");

    section.className =
        "battery-section";


    const title =
        document.createElement("h3");

    title.innerText = name;

    section.appendChild(title);


    // --------------------------------------------------
    // CONVERT VOLTAGE
    // --------------------------------------------------

    let voltage = "-";

    if (
        battery.voltage !== undefined &&
        battery.voltage !== null
    ) {

        voltage =
            (
                Number(battery.voltage) / 100
            ).toFixed(2) + " V";
    }


    // --------------------------------------------------
    // CURRENT
    // --------------------------------------------------

    let current = "-";

    if (
        battery.current !== undefined &&
        battery.current !== null
    ) {

        current =
            battery.current + " A";
    }


    // --------------------------------------------------
    // TEMPERATURE
    // --------------------------------------------------

    let temperature = "-";

    if (
        battery.temperature !== undefined &&
        battery.temperature !== null
    ) {

        temperature =
            battery.temperature + " °C";
    }


    // --------------------------------------------------
    // SOC
    // --------------------------------------------------

    let soc = "-";

    if (
        battery.soc !== undefined &&
        battery.soc !== null
    ) {

        soc =
            battery.soc + " %";
    }


    // --------------------------------------------------
    // SOH
    // --------------------------------------------------

    let soh = "-";

    if (
        battery.soh !== undefined &&
        battery.soh !== null
    ) {

        soh =
            battery.soh + " %";
    }


    // --------------------------------------------------
    // CELL DIFFERENCE
    // --------------------------------------------------

    let cellDiff = "-";

    if (
        battery.cellDiff !== undefined &&
        battery.cellDiff !== null
    ) {

        cellDiff =
            battery.cellDiff + " mV";
    }


    // --------------------------------------------------
    // CYCLE COUNT
    // --------------------------------------------------

    let cycleCount = "-";

    if (
        battery.cycleCount !== undefined &&
        battery.cycleCount !== null
    ) {

        cycleCount =
            battery.cycleCount;
    }


    // --------------------------------------------------
    // INFORMATION GRID
    // --------------------------------------------------

    section.innerHTML += `

        <div class="info-grid">

            <div>
                <span>BMS ID</span>
                <strong>${battery.bmsId || "-"}</strong>
            </div>

            <div>
                <span>Voltage</span>
                <strong>${voltage}</strong>
            </div>

            <div>
                <span>Current</span>
                <strong>${current}</strong>
            </div>

            <div>
                <span>SOC</span>
                <strong>${soc}</strong>
            </div>

            <div>
                <span>SOH</span>
                <strong>${soh}</strong>
            </div>

            <div>
                <span>Temperature</span>
                <strong>${temperature}</strong>
            </div>

            <div>
                <span>Cell Difference</span>
                <strong>${cellDiff}</strong>
            </div>

            <div>
                <span>Cycle Count</span>
                <strong>${cycleCount}</strong>
            </div>

            <div>
                <span>Errors</span>
                <strong>${battery.errors || "-"}</strong>
            </div>

        </div>

    `;


    // --------------------------------------------------
    // CELL VOLTAGES
    // --------------------------------------------------

    if (
        Array.isArray(battery.cellVoltages) &&
        battery.cellVoltages.length > 0
    ) {

        const cellTitle =
            document.createElement("h4");

        cellTitle.innerText =
            "Cell Voltages";

        section.appendChild(cellTitle);


        const cells =
            document.createElement("div");

        cells.className =
            "cell-grid";


        battery.cellVoltages.forEach(
            function (cellVoltage, index) {

                const cell =
                    document.createElement("div");

                cell.className =
                    "cell";

                const voltage =
                    (
                        Number(cellVoltage) / 1000
                    ).toFixed(3);

                cell.innerHTML = `
                    <span>Cell ${index + 1}</span>
                    <strong>${voltage} V</strong>
                `;

                cells.appendChild(cell);
            }
        );


        section.appendChild(cells);
    }


    return section;
}


// --------------------------------------------------
// REFRESH EVERY 3 SECONDS
// --------------------------------------------------

loadDevices();

setInterval(
    loadDevices,
    3000
);
