from widevine.cdm import CDM
from widevine.device import DEVICE
from widevine.pssh import PSSH
import base64
import requests
import json
import colorama
from colorama import Fore, Style

colorama.init()

pssh = "AAAAeXBzc2gAAAAA7e+LqXnWSs6jyCfc1R0h7QAAAFkIARIQPUD8NYa/THW755cHj6cOHhoGYW1hem9uIjVjaWQ6UFVEOE5ZYS9USFc3NTVjSGo2Y09IZz09LElsRnlrY2JsUXFlbWlNaitwQmJ3bnc9PUjj3JWbBg=="
data = {}
data = 'widevine2Challenge=CAESviAScQpvClkIARIQgcPgZDJTRmKrjbBVlVMTfxoGYW1hem9uIjVjaWQ6Z2NQZ1pESlRSbUtyamJCVmxWTVRmdz09LGVWZHE5clB6UjArSVQvZEZIeHB5aGc9PSoCU0QyABABGhB2oAAqF2QXvbvwB7AGQK3CGAEg2Oy9rwYwFjisnaeXCUKrHwoPYW1hem9uLmNvbS1wcm9kEhAK5BG1lFqxWAW3sMi9W1UcGvAcP6vB3lZHUIh1pqCRmylzLhxZ/pFq70580PJPIUmPrrqaF1jjNGohtq9alvzGtlnyTpmcCV2uCkD9FDEpHitA8YKdNGrH3px1A9UKZJDQ2SmYrLmDMLy0dI+TFBzk1NWI04D/5ttMaxzXzPYyNTXtDZ8LFg50c65/E2KfZMEQZe53WxU3NISZ2kG9V9HH6OXUT0ZjWjHTh0VeeCpAz20ARWXEcHorFnXM4QObNjMa+WZa2pwm9Ks4r6RijF41INHGkJAkzM0wqG8bcA1nAPwknJFmQ21RlvBRRDRtsWkyM8IlE9SD7Hft09wutih4G8GqlqZQwrufem5SqIEOTNVD+dMtbZ1bnQj3tPG24TzGAT/Fgq0bvWxBA8SLZ1qfRWwFzbZlIpELurMr8K7lqPU2fOHHugbG2NDiXxt7bdAXnOsEPU/oUKZUXTOvL9g5tkz0GNUlssDIX4fmcrOzpiEG+/EDFjxSa7dc5BVYJOLyt87nrQmfYvbNYaw3qqUF5LjPtstuMytYb+BaC+FSrd94AiZ+dPIYubfTm0ZLUlumsqOjh0u802wpAeAg0RvGXGsjEein4tui0ynw1wlig3ke+evh8/DBSlfDHwcT7jg3uCfPV5dMJgNRuAb9+i8BSX5tgrEWwjqc5hEcfLFHhsMHVUL0w99q+pCWutC7kTPgCXlgMYERhnFiy7fYnrnHtDmF+J6CJ4l9J94mRb7wsHvMhBXMxPb/VuKzi3DHNgSMPFKlzBj2Y7uVMOLFlAXun3qU5Y3AOKG80xCCk91wSXJMVuJvyxJIwru4cZhrau2EzcCeoXKBuSJhKruiwUQlOdq4GKJ+kz++NV1yyi3TxA6/aNGwuBU4s8lBXItwlhdItawkbj4CxOmCGCGinzqW1EEahpMl2T5exk2MO0ISZVgGAQaGI2FmUOUAwOQXRS+nBbr9/RKdWSUIknGQJx3C/JAcKXCEp/BBV5i9auEulBYxh9o69gchrSGdjSnKZ9uMn5FbdFiamfjetgPQfTJASYmQKFWcWfjqu97fiuKBAqHNyKY5NKUMWM8/RpNfqYBahRm8QTPTZIqKfcZrE7yWLIbdsg5cvRS4Vv4UWfO6/UDx+16EcthzRJlnaGQMxcrO+7g9yX7Hie07sHNfuE/KyridS2DwmHnA1b6zZqdILJQbkN2kVaympC4gKRiX6QvOthmMp6bts0MFK2RS9AZBPWkhoOMZ5HXNTu6Ol8X2EOk7NmyEaswXKhXtOVLQE3lZf5s9OqwRGez1g6M0lcCDrmdRNwC0FCB+cTUwhugKK9U8uj18ZeoB3XVetHYzdy9rzi9Vygu3568EmyhqKHQ8ipnELrkUTwsc3SN46huutq7nQERMVSpryAqhkahcjpJ/mKLZJTR4a15uITWufGG5/qtGNvIaA1IbS84y4fVt0B61e8I/GldbITFVgeT8/EcyWUAVhvttU0ICVedR5rXyHX+UgmwTkTlBdYChBeg7UKwXheONGwQ/O8qGCNL+j0GKXqSH3SyisOlXI7fnrZ0QxY1oS4MSsQjb1Ab5ozzK0/m4U74227KRS0CxZcpPY697dDy+lRqtqBUiedfriyc6EKNA3AtLwfUedtyTTOsZJtkM0D9xzdAemOlvVYp92Np9mR1bdRb8lZOmdGXk6PcKlirkJ4GKEiFHMYmIKfqFx6VrxTbQzirIfksAxcCuvhOJOxQ0gWEbOFzBOu04IMzWFaWTPlx6JbkecwMC9maTmIIvsf/KRlaUkUVbivkyra4aifPdLE9Jb3pb8U/uKl4NjYsl/xsvpu//0x3PtTgB8zCgBsljcS/jJZObeDklW30mqbILV5UO3RFILpEEst0qfGReAeBa9RUQG2MTdaYAr237RQNKg9GbmcT0sdtOBU26870epnqqkxrFm3E0n2yylsRAYW7jY8IB6g8fnvlm7Ert7eZOORu8ubLUas1f2l3Rwnv0v7ipyFOMX9fmJJ90xIG89nTarVqTgfWG7LDVdTD9aN1FicEbjTocSH5Xu8Wowjkot5SR905WFoGAd60YBm2JLkNphwAA3GGQzFXTnrulShoyGlkm7cQkKxQcur7bssJ6EsJe3wfyLnIULpOOSMJLmD2SS/Zq5iyFad4Xnz3IqmjTCsBncnaeGWeA4IR3FKXZr+1Tbt0DlPj4t7NPGqQCGYlwDjDBpL3Wfjy7bZIl07jy3hurlR1FaYb0VZzqbBqV4DsJj0JOs/omc9uYVrEL2mvzgqTnk1CbPzqBpusU4MapALAWr4zWo2XAqWYROrnwPX14/eaXvWo9hlJmj93o3oNtetGRBv+EClhGG17ElV6D9MsexYuW5gnNuYdLuyuEJQqJ9CDVO+uVohpUvha/TnkfptI56U0i0o0GAP8Me0ZS9inxLYy4/UVs3gDb03678ocCGHEtvD8cXSN1RkVpRosRzmlVYBlEELDZJGfWCx5eRNTE29ClRdnpm6JA9FC+yR6AsWJ3TgCXO4M1Y9HELaOB7bICqPKs/5TS0Bf+a5hrzr2412SY5tmqcCqYjwn9Wzpg1H1onpg02Oj5s8w8fBolaLpLp6cgHZWQODGO+gCScqFkQIBHydfqpV0jtR9e1zS2si0x1B3l7yJxpwv+qkhsxqzyUxEbYf8PbLUu6rocFxXuZl6L5UtMqaHvuRd7wjh20C5sjmrKi56me0eZJohIveKgx5gfldECMeRKCmGL0h7WxQoN/mw4BJOoabdIsSmPmo8d/rFe32eUUKjiuiOLOqOP0zilUKql1yvqnWqpCnEWBzpyuM0QtF8zHl1MGqtVMNN0OAuc2JfN7leXRpEUnnnPJt5w6bgkTdlg1bTQyEPunfhuPEWE1HGqVledCPkBrZ+XAnoXxAfqi0MWKrjPAxi71XUI4CZJG54V3dgGe0K/IAP8CvOejGd21R56LaoXjOwNSQyxj/l/LBSoSVptQQQ8p4IrP/yLchoSJY8heOyhXeV8fu3aTiX8H0D9LwBL8Kz7UtzXgkqNqclKNEsgDgX4fZMADPoMs4f1ikN2BjpvJ8vGbU9mJGCuZxHYgHRDTXWryyu+qNLXktINmH/D48Q9JCLeN7CdVLv5lC+Fle9AzJTJv7mNw5h6YbWwNcTgKUFJ3R4yoKwOTffQmRObmi47CRqGHqWei2nZ69EF6WgBiXEkBbKlpSmT8p+PdkEJgPJUGfZ/YtAWZBYECxEDz1Yb3LoGx/sBwLQKi9omyp7wvTK6Pvy4CQsn/l2e3Q5xlC4fEablsY5WL21HkIHVPvwubkHIpSwcY9sWgoI0gB4/viDyiTX/UCJHxbY2sHGryYgjmJcAP1uBp4tJNp4s7PWgknX/kGfxguqYQ/MOomb43S8B5hozwuhVWFDZz/LMX5uYcTzBOmjcS868yeyUVOOF+JcghIDt4H/OSxjpFfaOrvhusM8O867JU8zl1zL9ZMLeRnxf5E3vnbcaX80J8Knc2ryeE0OMo/zgUKOWuyKO1pPA7ZI0NaHZuh/v4wJs0uX9qopGlpd0y921uPL6FX7azUqYhtIMlN1wa5AiHL5oZ+TDJLKhHm6F/tnpjcWN4HlRzy62lEqMb5pA3/XsCzpY5XbAr0/YGcyeGtykzdo5dAI/s8kRcuq8/ERu4nSNzzsz43TeBN0g42s7vm/8CEvdQIf11VxAlQJeW1FVARQOVmzi7zp3nS4PAcUBJLWOCNqpjouUshpPQCvNmG0k4UqNEwzWiT7aJLl/k+0nO3F8yhHcaVxqFMqrOFcdnO9Kroshj10egT7N+rBddDydMuhRwv8o1nopB6osxDnbcByCmZr5bvBy80bze7fCS6ZGs+5vaWzcIEJnbJhJIsCRbm8aU2Sm8xrrn9A1sFMQgQ7kcf4oLqMQtt5LHzqVPFz9QkDXpufJx3ddNXhjeZ/PQmPn84W/9kMXr2R6pvc1lwq3BSeV+imEG/4e5JLf7AXsqawDq+4PH6arKOVkziYqSPTosQtuaN/POySi42KdMWsR+Ow5huuO0+SSA+Bd4njG5eEwESQkLCqvOo8FRei1OR1GlDhBonCQNlElgIZdPy5cCuuVuznWI715ZYDowr51olUfPA+OiMsMQPD6S60q2wcqO5pVyQ5izAkqaPkTP6QAmZslxEwKn3e1ELXKTRIqTjukwwNjjUZlr4qaaRadv5Vi0iTN9pEx2KY3Vf3VgIkDTg7/ayLbRASuTUxvXKI63vYZPSZWrffprb9q5VOG+0/U3vYjxlp1hnMQ+JadQJfx/eYrARs+fdUuI00/+UY6szk/3kL4TJTmvfhP1+4vX7Z95zfvbHzJy7EZBIXkRCkZ0QyDRobd0d9t2tC5CVCsuPvaisrkI/sAdZ4QA2pf+w7S2fkMInaxJicqVzLUq1/1s/D19citVBn1CB2m4QxwZegq+/AKtnrBvYR3fJ3uM1pXpf2Ho1bvp5anjurNQe8rKsFmVNZk+zlLOguJNIGhTtrrfGd56FptqG+KoNItZvHEjor8SBEsDfKhMA9xLQvGVv9lqiYW5J2QKZnrZMT6s0JU1RNFm6WG+6uxecD9dFcu7rtuEHphCYa9ROPYk5GQA3XuKc7hIN6c3WM+TUYtA08ejuvMfSL4r4S0iiitNB/kOP8sOmLi1jahjk3q3Pk2Q8e0AaPsT6R3e2Vmm8RbZBSodifeciNXGpYtLUQjmc05b6/RBJixfAAEX/ZtH4wUpoCd0iQKuEXXq3ne77V17/J0vyF82Ce4dS0cksPrKIGwbsMH8E0jEc7sdIhZhnQy3oo0Of43MxE8nDb6HK5luYWDAGq+4+Ks9gPlPmT44XAm58zc8K+ZRTUPzh4t085PkkPCuKg0cKHaxn+tOvm9Vy5iyWvsnwEOUvjLg1MYblr2PYbuIqr27NMU6rVsaiwJMhJ22eqp2kunlsvsCbKnqj4ICfC29It/kvnFIhB7uFSBPfweOhEV1/STHdQkKoACFTAT8q3uCL0rSJtu/70v0Q6h0+TI8QDar/l8tbVFDTryvwuRgwhYBMf0pGjr6hZmHKKu77ywoU77MVy9jnvn43Du19kZfUWthgJJiuWhRNx0VyJqvyWtC3Fykf2uSIh/siOLBtUV58Xx9AxLepdkMCY9vNJa/EYayNeAE8yv67YhuGUuP1aiEDpbvNFKpXZOyXtx78lrgDYvi7HrlGyqkTphRnXkZOXnPPWlkI0aO+vNm4lAfNY5uLNeU2c3fzA+7H5vrQvZuFP9B8vrahLsP6fMkEsDUpDHb4nIVpTqCnneQaSYpC/CvJKOC87vIG5kgYrREyBZIUPAwYqeMhqjFUoLNC4xMC4yNzEwLjAagAFcQfFc3npJHiDGokSA7fnOOyDTATUGGxcQYTAsoBNHdXkL6wL6P7IqCiitOlDxMhF9zP4M9EJhK06Ob9ad3TmegxW2mKcr/eG/FMU8LQzD+GeOfAmadicNhHqnRugRG1cgkJnPt8lDcpDD9Jetdn1EvkiSuGMojY4Cl4uSTm8shEoUAAAAAQAAABQABQAQkunOrOPhE6E=&includeHdcpTestKeyInLicense=true'
params = {
    'deviceID': '2fd64243-da3a-4ccc-aad7-77617707e27b',
    'deviceTypeID': 'AOAGZA014O5RE',
    'gascEnabled': 'true',
    'marketplaceID': 'A15PK738MTQHSO',
    'uxLocale': 'en_US',
    'firmware': '1',
    'playerType': 'xp',
    'operatingSystemName': 'Windows',
    'operatingSystemVersion': '10.0',
    'deviceApplicationName': 'Chrome',
    'asin': 'amzn1.dv.gti.f51fc4c7-a053-472a-ba54-ab7df1ad4955',
    'consumptionType': 'Streaming',
    'desiredResources': 'Widevine2License',
    'resourceUsage': 'ImmediateConsumption',
    'videoMaterialType': 'Feature',
    'clientId': 'f22dbddb-ef2c-48c5-8876-bed0d47594fd',
    'userWatchSessionId': 'c8a4168c-ce6e-476f-abb6-bddefb558198',
    'displayWidth': '1920',
    'displayHeight': '1080',
    'supportsVariableAspectRatio': 'true',
    'deviceProtocolOverride': 'Https',
    'vodStreamSupportOverride': 'Auxiliary',
    'deviceStreamingTechnologyOverride': 'DASH',
    'deviceDrmOverride': 'CENC',
    'deviceAdInsertionTypeOverride': 'SSAI',
    'deviceHdrFormatsOverride': 'None',
    'deviceVideoCodecOverride': 'H264',
    'deviceVideoQualityOverride': 'HD',
    'deviceBitrateAdaptationsOverride': 'CVBR,CBR',
    'playerAttributes': '{"middlewareName":"Chrome","middlewareVersion":"122.0.0.0","nativeApplicationName":"Chrome","nativeApplicationVersion":"122.0.0.0","supportedAudioCodecs":"AAC","frameRate":"HFR","H264.codecLevel":"4.2","H265.codecLevel":"0.0","AV1.codecLevel":"0.0"}',
}
headers = {
    'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
    'sec-ch-ua-platform': '"Windows"',
    'dnt': '1',
    'sec-ch-ua-mobile': '?0',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'content-type': 'application/x-www-form-urlencoded',
    'accept': '*/*',
    'origin': 'https://www.primevideo.com',
    'sec-fetch-site': 'same-site',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://www.primevideo.com/',
    # 'accept-encoding': 'gzip, deflate, br, zstd',
    'accept-language': 'en-US,en;q=0.9',
    # 'cookie': 'session-id=355-9228273-5723744; i18n-prefs=USD; ubid-main-av=355-1235108-6216739; lc-main-av=en_US; av-timezone=Asia/Singapore; av-profile=cGlkPWFtem4xLmFjdG9yLnBlcnNvbi5vaWQuQTIyNFpQWDdLWTgzT1AmdGltZXN0YW1wPTE3MTAwMjA4MjE4OTcmdmVyc2lvbj12MQ.g1HsXN7R7ofnElNEKmd3GTcwl9Ew0J1-UV724EpIZjLxAAAAAQAAAABl7NjVcmF3AAAAAPgWC9WfHH8iB-olH_E9xQ; x-main-av="UAOs97Ec4nivpo2vdul?CBN@BH9cyQbjENTRPBvv3toIeXoKKg7jd8wQj1bSDeFS"; at-main-av=Atza|IwEBIGRMh0VUSV_qspiKLjKjsvNC_4qWL0fRDmNvIxXKZrufnWCKxpuRujfRKyZHYCaNyIZ_1fwWLf5-iu7zJUtLZqPJ2bfWrYDNpA_n3m53R97TgQssQ1FgqhETNlFRrGLvJHTGDSHv_772w8I1nULOY17Gzp0hkwqZ_xlR9arLQ2RlUu3naDpc2Obss7GjpVrYgk7U15HCJePa3oAjz5eP9Z0iuWRN0NIU_lJESWX89C2Uyt_SYK3KL96NyA0T6rR1i1I; sess-at-main-av="NP/jYJbOJD4VslBLQ8ellUYVdH6tL/99Ex7LPZdET9s="; session-id-time=2082787201l; session-token="HRUCllvzdYOGT5LbWvmwfgfLghkvy/BfGxtp3zXg4HXWpptidOvfFwaNGksA8MkTNQUyNuh+4i40F1qkMZNAGtf2SSIwWVeSIsujqjjf9SNP/fs7Y1UkSdi/qnkOCFRTJQWFVWX37NW4x+RMBlUiF++GM5/br0gkleJNFvkybQ4SGhixD/Y0xEu0No+Gge1ZfWOkFo2RMz8dPdgJv+4lNM96v4B//2xKOzrLl0Fs7So7Abv2YBmDisBGiUdbI/0lCqRg7K1Uu5d/RpXTE9rE2q+NaVXtRxTwRsGsNCL+RODgN1aCR35TiKgeXtFKnT9XML8tAnkRmp8+Nz7kBEjJkOnnU5jGKgKa4KZ6Y4QETNhNjL1F6M/TiUwRqkGNd8u/TeF6PXnE4FQ="',
    'x-forwarded-for': '113.210.55.162',
    'X-AxDRM-Message': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ2ZXJzaW9uIjoxLCJjb21fa2V5X2lkIjoiYjMzNjRlYjUtNTFmNi00YWUzLThjOTgtMzNjZWQ1ZTMxYzc4IiwibWVzc2FnZSI6eyJ0eXBlIjoiZW50aXRsZW1lbnRfbWVzc2FnZSIsImZpcnN0X3BsYXlfZXhwaXJhdGlvbiI6NjAsInBsYXlyZWFkeSI6eyJyZWFsX3RpbWVfZXhwaXJhdGlvbiI6dHJ1ZX0sImtleXMiOlt7ImlkIjoiOWViNDA1MGQtZTQ0Yi00ODAyLTkzMmUtMjdkNzUwODNlMjY2IiwiZW5jcnlwdGVkX2tleSI6ImxLM09qSExZVzI0Y3Iya3RSNzRmbnc9PSJ9XX19.FAbIiPxX8BHi9RwfzD7Yn-wugU19ghrkBFKsaCPrZmU'
}
pssh = PSSH(pssh)
device = DEVICE.load("widevine/generic/widevine.wvd")
cdm = CDM.from_device(device)
session_id = cdm.open()
challenge = cdm.get_license_challenge(session_id, pssh)

urls = [
    "https://drm-playready-licensing.axtest.net/AcquireLicense",
            "https://discovery-us.conax.cloud/widevine/license",
            "https://proxy.staging.widevine.com",
            "https://cwip-shaka-proxy.appspot.com/no_auth",
            "https://drmv5-ax.learnyst.com/drmlicense/widevine",
            "https://drmv4-ax.learnyst.com/drmlicense/x-widevine",
            "https://drmv4-ax.learnyst.com/drmlicense/widevine",
            "https://evn73fp8.anycast.nagra.com/EVN73FP8/wvls/contentlicenseservice/v1/licenses",
            "https://lic.staging.drmtoday.com/license-proxy-widevine/cenc/",
            "https://sg-sg-sg.astro.com.my:9443/vgemultidrm/v1/widevine/license",
            "https://licensing.bitmovin.com/licensing",
            "https://license.vdocipher.com/auth",
            "https://license.uat.widevine.com/cenc/getlicense/widevine_test",
            "https://license.widevine.com/getlicense/",
            "https://license.uat.widevine.com/getlicense/",
            "https://playready.directtaps.net/pr/svc/rightsmanager.asmx",
            "https://fwp.nowe.com/wrapperWV"
            "http://msfrn-ci-cp-dev.mobitv.com/widevine/get_license",
            "http://test.playready.microsoft.com/directtaps/svc/pr152/rightsmanager.asmx",
            "http://test.playready.microsoft.com/directtaps/svc/pr20/rightsmanager.asmx",
            "http://test.playready.microsoft.com/directtaps/svc/pr21/rightsmanager.asmx",
            "http://test.playready.microsoft.com/directtaps/svc/pr29/rightsmanager.asmx",
            "http://test.playready.microsoft.com/directtaps/svc/pr30/rightsmanager.asmx",
            "http://test.playready.microsoft.com/service/rightsmanager.asmx",
            " https://license.pallycon.com/ri/licenseManager.do",
            "https://atv-ps-fe.primevideo.com/cdp/catalog/GetPlaybackResources?deviceID=2fd64243-da3a-4ccc-aad7-77617707e27b&deviceTypeID=AOAGZA014O5RE&gascEnabled=true&marketplaceID=A15PK738MTQHSO&uxLocale=en_US&firmware=1&playerType=xp&operatingSystemName=Windows&operatingSystemVersion=10.0&deviceApplicationName=Chrome&asin=amzn1.dv.gti.f51fc4c7-a053-472a-ba54-ab7df1ad4955&consumptionType=Streaming&desiredResources=Widevine2License&resourceUsage=ImmediateConsumption&videoMaterialType=Feature&clientId=f22dbddb-ef2c-48c5-8876-bed0d47594fd&userWatchSessionId=c8a4168c-ce6e-476f-abb6-bddefb558198&displayWidth=1920&displayHeight=1080&supportsVariableAspectRatio=true&deviceProtocolOverride=Https&vodStreamSupportOverride=Auxiliary&deviceStreamingTechnologyOverride=DASH&deviceDrmOverride=CENC&deviceAdInsertionTypeOverride=SSAI&deviceHdrFormatsOverride=None&deviceVideoCodecOverride=H264&deviceVideoQualityOverride=HD&deviceBitrateAdaptationsOverride=CVBR%2CCBR&playerAttributes=%7B%22middlewareName%22%3A%22Chrome%22%2C%22middlewareVersion%22%3A%22122.0.0.0%22%2C%22nativeApplicationName%22%3A%22Chrome%22%2C%22nativeApplicationVersion%22%3A%22122.0.0.0%22%2C%22supportedAudioCodecs%22%3A%22AAC%22%2C%22frameRate%22%3A%22HFR%22%2C%22H264.codecLevel%22%3A%224.2%22%2C%22H265.codecLevel%22%3A%220.0%22%2C%22AV1.codecLevel%22%3A%220.0%22%7D"
            "https://udrmv3.kaltura.com/cenc/widevine/license?custom_data=eyJjYV9zeXN0ZW0iOiJodHRwczovL3Jlc3QtYXMub3R0LmthbHR1cmEuY29tL2FwaV92My9zZXJ2aWNlL2Fzc2V0RmlsZS9hY3Rpb24vZ2V0Q29udGV4dD9rcz1kako4TXpJd09YeUYtazZMc1JVU05MTFcwNW9GNWktTmF5Nm04cFRuT2hSR0pZTTNOODNqSGd3eHBYY0JpOEJCa0tBeXRLQjE1ZDYyNENUcDljZHdqdWhhanJqV1lBVE5SRk5QbVBGWnNhakUzd1lraWJYVUNhel82UEZnUVhOSUV0UUxfS1dSSl9mbW5pelZUbm1sSnJtOHhIY243NmFMVkJocXFra0Q4bWhDVi1mOTUzVUpOc3RfZUROUUpHYnAtbGxYR0lyMWhKM1lLbzNzcDM5Yy1QVTJvREdiV2pSVlJjVlNuaVFZSTZuaUNWclVOa2loaGd4UnlLNnlNU3VXVzBJVnExQy1FWVUtWnZEM2U4emFwVWJValZtNVlmV19CRTBKdWE3UkxQR0U2eldvdUpXdHRhU0Rzd0VMN0phdU5xbHhlLTg2dlBXUGJIbnZwYUlUQncyUHJ6cVJqU2RyTy1PU2V3c1hIUnUyYWV1UWJoT2dXclhYZTBoa19LZ2hsVy1pMkgxeVdnb0pheE9ISnRjTlZuM2xJbmprQTZJTWJkdk8za2hqUGN5anNRdS1WU2VTU0pnbU12WVh3TFJHNUdTMmxDeDAxcnVsTVVXSkNvZU9DblpFazlfd1ZLeFl4eER0bm82OGJoMEZIYVRVZWU0ZFBRPT0mY29udGV4dFR5cGU9bm9uZSZpZD0xOTYwMDM5NiIsImFjY291bnRfaWQiOjMwODk2MzMsImNvbnRlbnRfaWQiOiIxX3h3N3lsb3J1XzFfZzd0d2xvajcsMV94dzd5bG9ydV8xX2t0bnBoMDFmLDFfeHc3eWxvcnVfMV9pYXg4eGwxaywxX3h3N3lsb3J1XzFfcGU1YWF0d3gsMV94dzd5bG9ydV8xXzJqMnZqcm53LDFfeHc3eWxvcnVfMV9semZxc2YzOCIsImZpbGVzIjoiIiwidXNlcl90b2tlbiI6ImRqSjhNekl3T1h5Ri1rNkxzUlVTTkxMVzA1b0Y1aS1OYXk2bThwVG5PaFJHSllNM044M2pIZ3d4cFhjQmk4QkJrS0F5dEtCMTVkNjI0Q1RwOWNkd2p1aGFqcmpXWUFUTlJGTlBtUEZac2FqRTN3WWtpYlhVQ2F6XzZQRmdRWE5JRXRRTF9LV1JKX2Ztbml6VlRubWxKcm04eEhjbjc2YUxWQmhxcWtrRDhtaENWLWY5NTNVSk5zdF9lRE5RSkdicC1sbFhHSXIxaEozWUtvM3NwMzljLVBVMm9ER2JXalJWUmNWU25pUVlJNm5pQ1ZyVU5raWhoZ3hSeUs2eU1TdVdXMElWcTFDLUVZVS1adkQzZTh6YXBVYlVqVm01WWZXX0JFMEp1YTdSTFBHRTZ6V291Sld0dGFTRHN3RUw3SmF1TnFseGUtODZ2UFdQYkhudnBhSVRCdzJQcnpxUmpTZHJPLU9TZXdzWEhSdTJhZXVRYmhPZ1dyWFhlMGhrX0tnaGxXLWkySDF5V2dvSmF4T0hKdGNOVm4zbEluamtBNklNYmR2TzNraGpQY3lqc1F1LVZTZVNTSmdtTXZZWHdMUkc1R1MybEN4MDFydWxNVVdKQ29lT0NuWkVrOV93Vkt4WXh4RHRubzY4YmgwRkhhVFVlZTRkUFE9PSIsInVkaWQiOiIwMTNjYmFlYS02ZjE4LTQ2NWMtYTFmNi05YmIyZDU4MDUzMmRfV0VCLTIxOWRmYjYyLTc5OTQtNTY2MC1kODNiLWRlYjBjNGM3NGUyYSIsImFkZGl0aW9uYWxfY2FzX3N5c3RlbSI6MzIwOX0%3d&signature=zG5rHqdA5eA4gYdr9W3YqcrDQpI%3d&sessionId=51e0b043-2cbd-0e09-b116-01993bcda89f:c4c57c1e-bad2-f748-eb14-1b972dfd4444&clientTag=html5:v8.03&referrer=aHR0cHM6Ly9zb29rYS5teS9lbi9wbGF5L21lbW9yaS1wYWplcmktbmFuYXMvMTU0NTkzMS9wbGF5ZXI="
]
for url in urls:
    try:
        data = {}
        challenge = b'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'
        data["widevine2Challenge"] = base64.b64encode(challenge).decode()
        # print(data["widevine2Challenge"])
        licence = requests.post(url, data=data, headers=headers)
        print(licence.text)
        licence.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"{Fore.RED}Error accessing {url}: {e}{Style.RESET_ALL}")
        continue

    try:
        cdm.parse_license(session_id, licence.content)
    except Exception as e:
        print(f"{Fore.RED}Error parsing license message from {url}: {e}{Style.RESET_ALL}")
        continue
    
    try:
        cdm.parse_license(session_id, licence.content)
    except requests.exceptions.ConnectionError as e:
        print(f"{Fore.RED}Error parsing license message from {url}: {e}{Style.RESET_ALL}")
        continue

    for key in cdm.get_keys(session_id):
        if key.type != 'SIGNING':
            kid = key.kid.hex()  # Add () to call the method
            key_value = key.key.hex()  # Add () to call the method
            print(f"{Fore.GREEN}[{key.type}] {kid}:{key_value}{Style.RESET_ALL}")

    cdm.close(session_id)
