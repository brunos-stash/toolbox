# import os
# import requests
from lxml import html

# import asyncio
# #import aiofiles
# from aiohttp import ClientSession


from aiohttp import ClientSession
import aiohttp
import asyncio
import async_timeout
from itertools import islice
import sys
import os
import FileHelper

ffzEmoteUrlStart = "https://cdn.frankerfacez.com/emoticon/"
ffzEmoteUrlEnd = "/1"
bttvEmoteUrlStart = "https://cdn.betterttv.net/emote/"
bttvEmoteUrlEnd = "/1x"


# def limited_as_completed(coros, limit):
#     futures = [
#         asyncio.ensure_future(c)
#         for c in islice(coros, 0, limit)
#     ]

#     async def first_to_finish():
#         while True:
#             await asyncio.sleep(0)
#             for f in futures:
#                 if f.done():
#                     futures.remove(f)
#                     try:
#                         newf = next(coros)
#                         futures.append(
#                             asyncio.ensure_future(newf))
#                     except StopIteration as e:
#                         pass
#                     return f.result()
#     while len(futures) > 0:
#         yield first_to_finish()


async def fetch(url, session):
    async with session.get(url) as response:
        # print(response.read())
        data = await response.read()
        b = html.fromstring(data)
        img_url = b.xpath(
            '/html/body/div/div/div[1]/div/form/table/tbody/tr[1]/td[3]/img/@src')
        # print(find)
        try:
            png_url = img_url[0][:-1]+str(1)
            # print(png_url)
        except:
            png_url = 'Not Found'
            # print('Not Found')
        return png_url


async def fetch2(url, session, name):
    # print(response.read())
    async with session.get(url) as response:
        # response = await s.get(url)
        data = await response.read()
        b = html.fromstring(data)
        img_url = b.xpath(
            '/html/body/div/div/div[1]/div/form/table/tbody/tr[1]/td[3]/img/@src')
        # print(find)
        try:
            png_url = img_url[0][:-1]+str(1)
            # print(png_url)
            await download_coroutine(png_url, session, name)
        except:
            png_url = 'Not Found'
            print('"{}" Not Found'.format(name))

        return png_url


async def fetch_page_emotes(url, session):
    # print(response.read())
    async with session.get(url) as response:
        # response = await s.get(url)
        data = await response.read()
        emote_row = 0
        b = html.fromstring(data)

        # print(find)

        for row in range(100):
            img_url = b.xpath(
                '/html/body/div/div/div[1]/div[1]/form/table/tbody/tr[{}]/td[3]/img/@src'.format(emote_row))
            img_name = b.xpath(
                '/html/body/div/div/div[1]/div[1]/form/table/tbody/tr[{}]/td[3]/img/@alt'.format(emote_row))
            if img_name:
                try:
                    # png_url = img_url[0][:-1]+str(1)
                    emote_row = row
                    # print('{} name:{}, url:{}'.format(
                    #    emote_row, img_name, img_url))
                    # print(png_url)
                    await download_coroutine(img_url[0], session, img_name[0])
                except:
                    # png_url = 'Not Found'
                    print('"{} {}" Not Found'.format(emote_row, img_url))
            else:
                emote_row = row

        # return png_url


async def bound_fetch(sem, url, session, name):
    # Getter function with semaphore.
    async with sem:
        # print('bound fetch')
        # return await fetch2(url, session, name)
        return await fetch_page_emotes(url, session)


async def run(url, emotelist):
    # url = "http://localhost:8080/{}"
    tasks = []
    # create instance of Semaphore
    sem = asyncio.Semaphore(100)

    # Create client session that will ensure we dont open new connection
    # per each request.
    async with ClientSession() as session:
        for i in emotelist:
            # pass Semaphore and session to every GET request
            task = asyncio.ensure_future(
                bound_fetch(sem, url.format(i), session, i))
            tasks.append(task)

        responses = asyncio.gather(*tasks)
        await responses
        print(responses)


async def run2(url, pages):
    # url = "http://localhost:8080/{}"
    tasks = []
    # create instance of Semaphore
    sem = asyncio.Semaphore(100)

    # Create client session that will ensure we dont open new connection
    # per each request.
    async with ClientSession() as session:
        for page in range(pages+1000):
            # pass Semaphore and session to every GET request
            task = asyncio.ensure_future(
                bound_fetch(sem, url.format(page), session, 'd'))
            tasks.append(task)

        responses = asyncio.gather(*tasks)
        await responses
        print(responses)

# async def print_when_done(tasks):
#     for res in limited_as_completed(tasks, limit):
#         await res


# async def emote_search(name_list, size):
#     ''' size = 1,2 oder 4
#     '''

#     base_url = 'https://www.frankerfacez.com/emoticons/?q='
#     for name in name_list:
#         search_url = '{0}{1}'.format(base_url, name)

#         async with ClientSession() as session:
#             async with session.get(search_url) as resp:
#                 data = await resp.read()

#         #a = requests.get(search_url)
#         b = html.fromstring(data)
#         img_url = b.xpath(
#             '/html/body/div/div/div[1]/div/form/table/tbody/tr[1]/td[3]/img/@src')
#         # print(find)
#         png_url = img_url[0][:-1]+str(size)
#         print(png_url)
    # return png_url


# def download(url, name, destination):
#     r = requests.get(url)
#     path = os.path.join(destination, name)
#     with open(path, 'wb') as fd:
#         tmp = 0
#         for chunk in r.iter_content(1024):
#             fd.write(chunk)
#             tmp += 1024
#             os.sys.stdout.write(f'\r{tmp/1000000:0.2f} MByte'.format(tmp))
#     print('\nFinished')
#     return

# async def download(url, name, destination):
#     r = requests.get(url)
#     path = os.path.join(destination, name)
#     with open(path, 'wb') as fd:
#         tmp = 0
#         for chunk in r.iter_content(1024):
#             fd.write(chunk)
#             tmp += 1024
#             os.sys.stdout.write(f'\r{tmp/1000000:0.2f} MByte'.format(tmp))
#     print('\nFinished')
#     return

async def download_coroutine(url, session, name):
    fold = 'C:\\Users\\BIGNIG\\Desktop\\memes\\'
    # with async_timeout.timeout(10):
    async with session.get(url) as response:
        filename = fold+name+'.png'
        # filename = fold+'AA'
        progress = 0
        with open(filename, 'wb') as f_handle:
            while True:
                sys.stdout.write(
                    '\rDownloading {}: {} KB'.format(name, progress))
                chunk = await response.content.read(1024)
                if not chunk:
                    break
                f_handle.write(chunk)
                progress += 1024
        print('')
        return await response.release()


async def async_downloader(url, name, filetype='png'):
    # fold = 'C:\\Users\\BIGNIG\\Desktop\\memes\\'
    # with async_timeout.timeout(10):
    async with ClientSession() as session:
        async with session.get(url) as response:
            filename = '{0}.{1}'.format(name, filetype)
            # filename = fold+'AA'
            progress = 0
            with open(filename, 'wb') as f_handle:
                while True:
                    sys.stdout.write(
                        '\rDownloading {}: {} KB'.format(name, progress))
                    chunk = await response.content.read(1024)
                    if not chunk:
                        break
                    f_handle.write(chunk)
                    progress += 1024
        print('')
        return await response.release()


class BetterTTVFinder:
    def __init__(self):
        self.bttvEmoteUrlStart = "https://cdn.betterttv.net/emote/"
        self.bttvEmoteUrlEnd = "/1x"

        # self.twitchEmoteUrlStart = "https://static-cdn.jtvnw.net/emoticons/v1/"
        # self.twitchEmoteUrlEnd = "/1.0"

    # async def fetch(self, url, session):
    #     # print(response.read())
    #     async with session.get(url) as response:
    #         # response = await s.get(url)
    #         # data = await response.read()
    #         # b = html.fromstring(data)

    #         try:

    #             await download_coroutine(img_url[0], session, img_name[0])
    #         except:
    #             png_url = 'Not Found'
    #             print('"{} {}" Not Found'.format(emote_row, img_url))

    async def bound_fetch(self, sem, url, session, name):
        # Getter function with semaphore.
        async with sem:
            # print('bound fetch')
            # return await fetch2(url, session, name)
            return await self.download_coroutine(url, session, name)

    async def download_coroutine(self, url, session, name):
        fold = 'C:\\Users\\BIGNIG\\Desktop\\memes\\'
        # with async_timeout.timeout(10):
        async with session.get(url) as response:
            filename = fold+name+'.png'
            # filename = fold+'AA'
            progress = 0
            # print(url)
            with open(filename, 'wb') as f_handle:
                while True:
                    sys.stdout.write(
                        '\rDownloading {}: {} KB'.format(name, progress))
                    chunk = await response.content.read(1024)
                    if not chunk:
                        break
                    f_handle.write(chunk)
                    progress += 1024
            print('')
            return await response.release()

    async def run(self, amount):
        # url = "http://localhost:8080/{}"
        tasks = []
        bttv_dict = FileHelper.JSONread(
            'C:\\Users\\BIGNIG\\Documents\\Python Scripts\\FrankerFaceZ\\emotedata_bttv.json')
        # create instance of Semaphore
        sem = asyncio.Semaphore(100)

        # Create client session that will ensure we dont open new connection
        # per each request.
        # self.amount = amount
        async with ClientSession() as session:
            # pass Semaphore and session to every GET request
            found = False
            for emote in bttv_dict.keys():
                if emote == 'LXHeart':
                    found = True
                if found:
                    # if self.amount > 0:
                    url = self.bttvEmoteUrlStart + \
                        bttv_dict[emote]+self.bttvEmoteUrlEnd
                    task = asyncio.ensure_future(
                        self.bound_fetch(sem, url, session, emote))
                    tasks.append(task)
                # self.amount -= 1
                # else:
                #     break
                else:
                    print('Skipping {}'.format(emote))
            responses = asyncio.gather(*tasks)
            await responses
            print(responses)

    def start(self, amount):
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(self.run(amount))
        loop.run_until_complete(future)


class EmoteJsonUpdater:
    # global_emotes_url = 'https://static-cdn.jtvnw.net/emoticons/v1/{image_id}/1.0'
    global_emotes_url = 'https://twitchemotes.com/emotes/{}'
    name_xpath = '/html/body/div[3]/div[1]/h2/text()'
    official_api_subscriber_emotes = 'https://twitchemotes.com/api_cache/v3/subscriber.json'
    json = {}

    @classmethod
    async def fetch_emote_name(cls, url, session, image_id):
        # print(response.read())
        async with session.get(url) as r:
            # response = await s.get(url)
            data = await r.read()
            if r.status == 200:
                content = html.fromstring(data)
                emote_name = content.xpath(cls.name_xpath)[0]
                print('{}:{}'.format(image_id, emote_name))
                return [emote_name, image_id]
            else:
                print('{}:None'.format(image_id))
                return None

    @classmethod
    async def bound_fetch(cls, sem, url, session, image_id):
        # Getter function with semaphore.
        async with sem:
            # print('bound fetch')
            # return await fetch2(url, session, name)
            return await cls.fetch_emote_name(url, session, image_id)

    @classmethod
    async def run(cls):
        tasks = []
        json = FileHelper.JSONread('updated_emotes.json')
        sem = asyncio.Semaphore(500)
        async with ClientSession() as session:
            json_start = max(json.values())
            for image_id in range(json_start, 500000):
                # pass Semaphore and session to every GET request
                task = asyncio.ensure_future(cls.bound_fetch(
                    sem, cls.global_emotes_url.format(image_id), session, image_id))
                tasks.append(task)

            responses = asyncio.gather(*tasks)
            await responses
            for response in responses._result:
                if response is not None:
                    json[response[0]] = response[1]
            print(json)
            FileHelper.JSONwrite('updated_emotes.json', json)


if __name__ == '__main__':
    emotelist = ['monka', 'monkaMEGA', 'monkaS',
                 'monkaGIGA', 'monkaOMEGA', 'monkaASS', 'gachiGasm', 'gachiBASS', 'Pog', 'POGGERS', 'HYPERS', 'HYPERBRUH', 'HYPERPOGCHAMP']
    # emotelist = ['gachiBASS']
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(emote_search(emotelist, 1))
    # # download(emote, 'dd.png', 'C:\\Users\\BIGNIG\\Desktop\\memes')

    # r = int(sys.argv[1])
    # url = "https://www.frankerfacez.com/emoticons/?q={}"
    # url = 'https://www.frankerfacez.com/emoticons/?q=&sort=count-desc&page={}'

    # loop = asyncio.get_event_loop()
    # with ClientSession() as session:

    # future = asyncio.ensure_future(run2(url, 1))
    # loop.run_until_complete(future)

    # bttv = BetterTTVFinder()
    # bttv.start(10)
    # read = FileHelper.JSONread('emotedata_twitch_global.json')
    # print(read['emotes'].keys())

    # twitch = OfficialEmotes()
    # emote = Emote()
    # e = twitch.get_emote_url(25, size='large')
    # print(e)
    # if not emote.is_in_folder('Kappa'):
    #     twitch.download_emote('Kappa')
    # else:
    #     print('Emote is available')

    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(EmoteJsonUpdater().run())
    loop.run_until_complete(future)
