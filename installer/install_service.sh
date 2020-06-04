#!/bin/bash
cat > /lib/systemd/system/${2}.service <<-EOF
[Unit]
Description=${2}
After=network.target

[Service]
User=${1}
LimitNPROC=infinity
LimitNOFILE=infinity
LimitFSIZE=infinity
LimitCPU=infinity
LimitAS=infinity
ExecStart=/bin/bash /home/${1}/${2}/run_gunicorn.sh ${2} ${3}
ExecStop=/bin/bash /home/${1}/${2}/stop_gunicorn.sh ${2} ${3}

[Install]
WantedBy=multi-user.target
EOF
