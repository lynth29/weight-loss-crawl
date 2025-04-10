import asyncio
import aiohttp
import json
from utils import save_csv

api = "https://api.chloeting.com/app/program/{}/weeks/{}/days/{}/videos?userId="
all_results = []


async def fetch(session, challenge_id: str, week_num: int, week_day: int):
    url = api.format(challenge_id, week_num, week_day)
    try:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                for video in data:
                    video = video.get("video")
                    info = {
                        "day": week_num * 7 + week_day + 1,
                        "title": video.get("programScheduleTitle"),
                        "short_title": (
                            video.get("displayTags")[0]["title"]
                            if video.get("displayTags")
                            else None
                        ),
                        "workout_length": video.get("workoutLength"),
                        "workout_types": (
                            video.get("workoutTypes")[0]
                            if video.get("workoutTypes")
                            else None
                        ),
                        "secondary_types": (
                            ", ".join(video.get("secondaryTypes"))
                            if video.get("secondaryTypes")
                            else None
                        ),
                        "url": video.get("url"),
                    }
                    all_results.append(info)
                    print(f"Finish fetching  {week_day+1} of week {week_num}")
            else:
                print(
                    f"Failed to fetch day {week_day+1} of week {week_num}: Status code {response.status}"
                )
    except Exception as e:
        print(f"Error for day {week_day+1} of week {week_num}: {e}")
    await asyncio.sleep(1)  # wait before next week


async def main(challenge_id: str):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for week in range(6):
            for day in range(7):
                print(f"Fetching day {day+1} of week {week+1}")
                tasks.append(fetch(session, challenge_id, week, day))
        await asyncio.gather(*tasks)

    save_csv(all_results, "./output/output.csv")
    print("Done")


if __name__ == "__main__":
    asyncio.run(main(challenge_id="6768561e16f27b176905c218"))
