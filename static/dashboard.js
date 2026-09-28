async function loadDevices() {

    try {

        const response =
            await fetch("/api/devices");

        const devices =
            await response.json();

        const container =
            document.getElementById("deviceList");

        container.innerHTML = "";

        const deviceIds =
            Object.keys(devices);

        if (deviceIds.length === 0) {

            container.innerHTML =
                "<p>No T-Box data received yet.</p>";

            return;
        }

        deviceIds.forEach(function(id) {

            const d = devices[id];

            const card =
                document.createElement("div");

            card.className = "device";

            card.innerHTML = `

                <div class="device-title">
                    T-Box: ${d.tboxId || id}
                </div>

                <div class="data-grid">

                    <div class="data-item">
                        <div class="label">
                            Battery Voltage
                        </div>
                        <div class="value">
                            ${d.BatVoltage ?? "-"} V
                        </div>
                    </div>

                    <div class="data-item">
                        <div class="label">
                            Battery Current
                        </div>
                        <div class="value">
                            ${d.BatCurrent ?? "-"} A
                        </div>
                    </div>

                    <div class="data-item">
                        <div class="label">
                            SOC
                        </div>
                        <div class="value">
                            ${d.SOC ?? "-"} %
                        </div>
                    </div>

                    <div class="data-item">
                        <div class="label">
                            SOH
                        </div>
                        <div class="value">
                            ${d.SOH ?? "-"} %
                        </div>
                    </div>

                    <div class="data-item">
                        <div class="label">
                            Motor RPM
                        </div>
                        <div class="value">
                            ${d.MotorRPM ?? "-"}
                        </div>
                    </div>

                    <div class="data-item">
                        <div class="label">
                            State
                        </div>
                        <div class="value">
                            ${d.state ?? "-"}
                        </div>
                    </div>

                    <div class="data-item">
                        <div class="label">
                            Distance
                        </div>
                        <div class="value">
                            ${d.total_distance_km ?? "-"} km
                        </div>
                    </div>

                </div>
            `;

            container.appendChild(card);
        });

    } catch (error) {

        console.error(error);

    }
}

loadDevices();

setInterval(loadDevices, 5000);
