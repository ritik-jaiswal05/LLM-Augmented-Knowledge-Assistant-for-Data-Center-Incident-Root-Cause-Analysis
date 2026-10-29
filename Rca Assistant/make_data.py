"""Generates SYNTHETIC incident/runbook documents into data/kb/ (labelled synthetic)."""
import json, os
DOCS = [
("INC-001","network","Core switch uplink flapping","Users report intermittent packet loss. Switch logs show interface Gi0/1 link up/down every few seconds and CRC errors rising.","Faulty fiber transceiver or damaged patch cable on the uplink.","Check SFP optical power levels; replace patch cable; swap transceiver; review CRC counters."),
("INC-002","network","BGP session down after config change","Traffic to external networks dropped right after a maintenance window. BGP neighbor state stuck in Idle, route table shows missing prefixes.","Misconfigured BGP neighbor ASN / route policy introduced in the change.","Diff the running config against last backup; verify neighbor ASN; roll back the change; check route filters."),
("INC-003","network","DNS resolution failures","Applications time out resolving hostnames. nslookup against internal resolver returns SERVFAIL; resolver CPU is normal.","Upstream DNS forwarder unreachable or zone data corrupted.","Query forwarder directly; check zone transfer status; restart resolver; fail over to secondary DNS."),
("INC-004","storage","Disk full on database server","Database writes fail with 'No space left on device'. df shows /var at 100%. Binary logs and old backups are large.","Log and backup retention not rotated, filling the data volume.","Run df -h and du to find large directories; purge old logs; fix logrotate; add disk usage alerting."),
("INC-005","storage","RAID array degraded","Storage controller raised a degraded-array alert. One disk marked failed, read latency increased, rebuild in progress.","Physical disk failure in the RAID group.","Check controller logs and SMART data; replace failed drive; monitor rebuild; verify backups are current."),
("INC-006","storage","NFS mount hangs","Application servers freeze on file access. Mount shows 'server not responding'. NFS server load is very high with many stuck threads.","NFS server overloaded or network path to the NFS server impaired.","Check NFS server load and nfsstat; verify network path and MTU; remount with soft options as a temporary measure."),
("INC-007","cooling","Rack inlet temperature alarm","Temperature alert from rack C12: inlet temp above 32C. Several servers throttled CPU frequency. CRAC unit 3 showing fault.","CRAC unit failure reducing cold-aisle airflow.","Inspect CRAC unit status and compressor; check blocked floor tiles; move load away from hot racks; engage facilities."),
("INC-008","cooling","Hot spot due to blanking panel gaps","One server row runs hotter than others while room temperature is normal. Missing blanking panels observed in rack.","Hot-air recirculation caused by missing blanking panels.","Walk the aisle with a thermal camera; install blanking panels; verify containment doors are closed."),
("INC-009","power","UPS on battery after utility outage","Power alarm: UPS switched to battery mode, runtime countdown active. Utility feed lost, generator has not started.","Utility power loss with generator auto-start failure.","Check ATS and generator status; start generator manually; shed non-critical load; monitor UPS runtime."),
("INC-010","power","PDU circuit breaker tripped","Several servers in one rack went offline simultaneously. PDU shows breaker B2 tripped, load was near rated maximum.","Circuit overload on the PDU branch after new servers were added.","Check PDU load per outlet; redistribute servers across phases; reset breaker only after load is reduced."),
("INC-011","service","Application crash loop after deploy","Web service restarts repeatedly after release 4.2. Logs show NullPointerException on startup and health check failing.","Faulty release with a missing configuration value.","Compare config of 4.2 vs 4.1; check startup stack trace; roll back release; add config validation to CI."),
("INC-012","service","Out-of-memory kills on service host","Service process killed by OOM killer. dmesg shows 'Out of memory: Killed process'. Memory usage grew steadily for days.","Memory leak in the application.","Review memory growth in monitoring; capture heap dump; restart service as mitigation; set memory limits and alert."),
("INC-013","latency","High latency from database connection pool exhaustion","API response time rose from 100ms to 5s. Logs show 'timeout waiting for connection from pool'. Database CPU is low.","Connection pool exhausted by slow queries or leaked connections.","Check active vs max connections; find long-running queries; fix connection leaks; tune pool size."),
("INC-014","latency","Latency spike from noisy neighbour VM","One VM shows slow disk and CPU steal time above 20% while its own load is low. Other VMs on the same host are busy.","Resource contention from a noisy neighbour on the same hypervisor host.","Check CPU steal and host utilisation; migrate VM to another host; apply resource limits to the noisy tenant."),
("INC-015","service","Certificate expired causing TLS failures","Clients get TLS handshake errors. Browser reports expired certificate. Service itself is running normally.","Expired TLS certificate not renewed.","Check certificate expiry with openssl; renew and deploy certificate; add expiry monitoring."),
("INC-016","network","Packet loss from MTU mismatch","Large transfers stall while pings succeed. Fragmentation needed messages seen after a VLAN change.","MTU mismatch between two network segments.","Test with ping -M do -s sizes; compare MTU on both ends; align MTU settings."),
]
os.makedirs("data/kb", exist_ok=True)
for id_, cat, title, symptoms, cause, steps in DOCS:
    with open(f"data/kb/{id_}.md","w") as f:
        f.write(f"[SYNTHETIC] {title}\nCategory: {cat}\nSymptoms: {symptoms}\nRoot cause: {cause}\nDiagnostic steps: {steps}\n")
# held-out test incidents: written differently from KB docs, labelled by category + expected cause keyword
TESTS = [
 ("Ping works but big file copies between two VLANs hang after yesterday's change","network","mtu"),
 ("Optical errors and the uplink keeps going up and down, lots of CRC counters","network","transceiver"),
 ("Cannot resolve internal hostnames, SERVFAIL from our resolver","network","dns"),
 ("/var is 100% full and the database refuses writes","storage","disk"),
 ("Controller says one drive failed and the array is rebuilding, reads are slow","storage","raid"),
 ("File servers mounted over NFS are frozen, 'not responding'","storage","nfs"),
 ("Rack row temperature alarm, servers throttling, air conditioning unit fault","cooling","crac"),
 ("Whole rack lost power at once, PDU shows tripped breaker near max load","power","overload"),
 ("Building lost mains, UPS is running on batteries and the generator did not start","power","generator"),
 ("After the new release the service keeps restarting with a null pointer on startup","service","release"),
 ("Process killed by OOM killer, memory kept growing for days","service","memory"),
 ("API calls take 5 seconds, 'timeout waiting for connection from pool', DB CPU idle","latency","pool"),
]
json.dump([{"query":q,"category":c,"keyword":k} for q,c,k in TESTS], open("data/tests.json","w"), indent=2)
print(f"Wrote {len(DOCS)} synthetic docs and {len(TESTS)} test cases")
