import json
base = "https://www.boi.org.il/en/communication-and-publications/press-releases/"

longslugs = {
"2018-01-10":("20231130034252","the-monetary-committee-decides-on-january-10-2018-to-keep-the-interest-rate-unchanged-at-01-percent"),
"2018-02-26":("20231210015007","the-monetary-committee-decides-on-february-26-2018-to-keep-the-interest-rate-unchanged-at-01-percent"),
"2018-04-16":("20231201010415","the-monetary-committee-decides-on-april-16-2018-to-keep-the-interest-rate-unchanged-at-01-percent"),
"2018-05-28":("20231130035644","the-monetary-committee-decides-on-may-28-2018-to-keep-the-interest-rate-unchanged-at-01-percent"),
"2018-07-09":("20231130074312","the-monetary-committee-decides-on-july-9-2018-to-keep-the-interest-rate-unchanged-at-01-percent"),
"2018-08-29":("20230205065838","the-monetary-committee-decides-on-august-29-2018-to-keep-the-interest-rate-unchanged-at-01-percent"),
"2018-10-08":("20231209052442","the-monetary-committee-decides-on-october-8-2018-to-keep-the-interest-rate-unchanged-at-01-percent"),
"2018-11-26":("20230205084104","the-monetary-committee-decides-on-november-26-2018-to-increase-the-interest-rate-by-015-percentage-points-to-025-percent"),
"2019-01-07":("20230206115612","the-monetary-committee-decides-on-january-7-2019-to-keep-the-interest-rate-unchanged-at-025-percent"),
"2019-02-25":("20231202223509","the-monetary-committee-decides-on-february-25-2019-to-keep-the-interest-rate-unchanged-at-025-percent"),
"2019-04-08":("20231202050351","the-monetary-committee-decides-on-april-8-2019-to-keep-the-interest-rate-unchanged-at-025-percent"),
"2019-05-20":("20231203041910","the-monetary-committee-decides-on-may-20-2019-to-keep-the-interest-rate-unchanged-at-025-percent"),
"2019-07-08":("20230206133300","the-monetary-committee-decides-on-july-8-2019-to-keep-the-interest-rate-unchanged-at-025-percent"),
"2019-08-28":("20231207135430","the-monetary-committee-decides-on-august-28-2019-to-keep-the-interest-rate-unchanged-at-025-percent"),
"2019-10-07":("20231202220423","the-monetary-committee-decides-on-october-7-2019-to-keep-the-interest-rate-unchanged-at-025-percent"),
"2019-11-25":("20230201121425","the-monetary-committee-decides-on-november-25-2019-to-keep-the-interest-rate-unchanged-at-025-percent"),
"2020-01-09":("20230201220237","the-monetary-committee-decides-on-january-9-2020-to-keep-the-interest-rate-unchanged-at-025-percent"),
"2020-02-24":("20230131194640","the-monetary-committee-decides-on-february-24-2020-to-keep-the-interest-rate-unchanged-at-025-percent"),
"2020-04-06":("20230201122447","the-monetary-committee-decides-on-april-6-2020-to-reduce-the-interest-rate-by-015-percentage-points-to-01-percent"),
"2020-05-25":("20230205071841","the-monetary-committee-decides-on-may-25-2020-to-keep-the-interest-rate-unchanged-at-01-percent"),
"2020-07-06":("20230206162544","the-monetary-committee-decides-on-july-6-2020-to-keep-the-interest-rate-unchanged-at-01-percent"),
"2020-08-24":("20230131030743","the-monetary-committee-decides-on-august-24-2020-to-keep-the-interest-rate-unchanged-at-01-percent"),
"2020-10-22":("20231208151734","the-monetary-committee-decides-on-october-22-2020-to-keep-the-interest-rate-unchanged-at-01-percent"),
"2020-11-30":("20230129053303","the-monetary-committee-decides-on-november-30-2020-to-keep-the-interest-rate-unchanged-at-01-percent"),
"2021-01-04":("20230208200957","the-monetary-committee-decides-on-january-4-2021-to-keep-the-interest-rate-unchanged-at-01-percent"),
"2021-02-22":("20230206005127","the-monetary-committee-decides-on-february-22-2021-to-keep-the-interest-rate-unchanged-at-01-percent"),
"2021-04-19":("20231208155409","the-monetary-committee-decides-on-april-19-2021-to-keep-the-interest-rate-unchanged-at-01-percent"),
"2021-05-31":("20230204212218","the-monetary-committee-decides-on-may-31-2021-to-keep-the-interest-rate-unchanged-at-01-percent"),
"2021-07-05":("20230201222709","the-monetary-committee-decides-on-july-5-2021-to-keep-the-interest-rate-unchanged-at-01-percent"),
"2021-08-23":("20231203042507","the-monetary-committee-decides-on-august-23-2021-to-keep-the-interest-rate-unchanged-at-01-percent"),
"2021-10-07":("20230129080944","the-monetary-committee-decides-on-october-7-2021-to-keep-the-interest-rate-unchanged-at-01-percent"),
"2021-11-22":("20231202062915","the-monetary-committee-decides-on-november-22-2021-to-keep-the-interest-rate-unchanged-at-01-percent"),
"2022-01-03":("20231203130224","the-monetary-committee-decides-on-january-3-2022-to-keep-the-interest-rate-unchanged-at-01-percent"),
"2022-02-21":("20231210204050","the-monetary-committee-decides-on-february-21-2022-to-keep-the-interest-rate-unchanged-at-01-percent"),
"2022-04-11":("20231204185927","the-monetary-committee-decides-on-april-11-2022-to-increase-the-interest-rate-to-035-percent"),
"2022-05-23":("20230128072139","the-monetary-committee-decides-on-may-23-2022-to-increase-the-interest-rate-to-075-percent"),
"2022-07-04":("20231208154450","the-monetary-committee-decides-on-july-4-2022-to-increase-the-interest-rate-by-05-percentage-points-to-125-percent"),
"2022-08-22":("20230201120444","the-monetary-committee-decides-on-august-22-2022-to-increase-the-interest-rate-by-075-percentage-points-to-2-percent"),
"2022-10-03":("20230129045750","the-monetary-committee-decides-on-october-3-2022-to-increase-the-interest-rate-by-075-percentage-points-to-275"),
"2022-11-21":("20221220193232","the-monetary-committee-decides-on-november-21-2022-to-increase-the-interest-rate-by-05-percentage-points-to-325-percent"),
"2023-01-02":("20230102203129","the-monetary-committee-decides-on-january-2-2023-to-increase-the-interest-rate-by-05-percentage-points-to-375-percent"),
"2023-02-20":("20230221073224","the-monetary-committee-decides-on-february-20-2023-to-increase-the-interest-rate-by-05-percentage-points-to-425-percent"),
"2023-04-03":("20230404045140","the-monetary-committee-decides-on-april-3-2023-to-increase-the-interest-rate-by-025-percentage-points-to-45-percent"),
"2023-05-22":("20230522192701","the-monetary-committee-decides-on-may-22-2023-to-increase-the-interest-rate-by-025-percentage-points-to-475-percent"),
"2023-07-10":("20230711015741","the-monetary-committee-decides-on-july-10-2023-to-leave-the-interest-rate-unchanged-at-475-percent"),
"2024-02-26":("20240226203957","the-monetary-committee-decides-on-february-26-2024-to-leave-the-interest-rate-unchanged-at-45-percent"),
"2024-04-08":("20240412215409","the-monetary-committee-decides-on-april-8-2024-to-leave-the-interest-rate-unchanged-at-45-percent"),
"2024-05-27":("20240527201628","the-monetary-committee-decides-on-may-27-2024-to-leave-the-interest-rate-unchanged-at-45-percent"),
"2024-07-08":("20240709102425","the-monetary-committee-decides-on-july-8-2024-to-leave-the-interest-rate-unchanged-at-45-percent"),
"2024-08-28":("20240828213421","the-monetary-committee-decides-on-august-28-2024-to-leave-the-interest-rate-unchanged-at-45-percent"),
"2024-10-09":("20241028204519","the-monetary-committee-decides-on-october-9-2024-to-leave-the-interest-rate-unchanged-at-45-percent"),
"2025-02-24":("20250224213347","the-monetary-committee-decides-on-february-24-2025-to-leave-the-interest-rate-unchanged-at-45-percent"),
"2025-04-07":("20250407194813","the-monetary-committee-decides-on-april-7-2025-to-leave-the-interest-rate-unchanged-at-45-percent"),
"2025-05-26":("20250526233131","the-monetary-committee-decides-on-may-26-2025-to-leave-the-interest-rate-unchanged-at-45-percent"),
"2025-07-07":("20250707205255","the-monetary-committee-decides-on-july-7-2025-to-leave-the-interest-rate-unchanged-at-45-percent"),
"2025-09-29":("20250930181634","the-monetary-committee-decides-on-september-29-2025-to-leave-the-interest-rate-unchanged-at-45-percent"),
"2026-03-30":("20260405164326","the-monetary-committee-decides-on-march-30-2026-to-leave-the-interest-rate-unchanged-at-400-percent"),
"2026-07-06":("20260708132246","the-monetary-committee-decides-on-july-6-2026-to-lower-the-interest-rate-to-35-percent"),
}

cands = {
"2023-09-04":[("20231014044624","a04-09-23")],
"2023-10-23":[("20231023185358","b23-10-23")],
"2023-11-27":[("20231128105633","a27-11-23")],
"2024-01-01":[("20240101180526","a01-01-24")],
"2024-11-25":[("20241127042954","25-11-24")],
"2025-01-06":[("20250118082502","6-1-25")],
"2025-08-20":[("20250820195835","20-8-25-en")],
"2025-11-24":[("20251124204625","24-11-25-en")],
"2026-01-05":[("20260106120750","05-01-25a-en"),("20260106120233","5-1-25-en"),("20260108042120","7-1-25en")],
"2026-02-23":[("20260412090107","23-2-26-en")],
"2026-05-25":[("20260525131402","25-05-2026")],
}

work = []
for d,(ts,slug) in sorted(longslugs.items()):
    work.append({"id":d,"wb":["https://web.archive.org/web/%sid_/%s%s/" % (ts,base,slug)],"status":"known"})
for d,lst in sorted(cands.items()):
    work.append({"id":d,"wb":["https://web.archive.org/web/%sid_/%s%s/" % (ts,base,slug) for ts,slug in lst],"status":"candidate"})

json.dump(work, open("scripts/worklist.json","w"), indent=1)
print(len(work),"entries;", sum(1 for w in work if w['status']=='known'),"known;", sum(1 for w in work if w['status']=='candidate'),"candidate")
