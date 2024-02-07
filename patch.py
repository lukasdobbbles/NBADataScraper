#!/usr/bin/python
import logging
import time
import re
import io

executable_path = '/home/backyardsubsistence/.local/share/undetected_chromedriver/undetected_chromedriver'

def patch_exe():
        start = time.perf_counter()
        logging.info("patching driver executable %s" % executable_path)
        with io.open(executable_path, "r+b") as fh:
            content = fh.read()
            # match_injected_codeblock = re.search(rb"{window.*;}", content)
            match_injected_codeblock = re.search(rb"\{window\.cdc.*?;\}", content)
            if match_injected_codeblock:
                target_bytes = match_injected_codeblock[0]
                new_target_bytes = (
                    b'{console.log("undetected chromedriver 1337!")}'.ljust(
                        len(target_bytes), b" "
                    )
                )
                new_content = content.replace(target_bytes, new_target_bytes)
                if new_content == content:
                    logging.warning(
                        "something went wrong patching the driver binary. could not find injection code block"
                    )
                else:
                    logging.debug(
                        "found block:\n%s\nreplacing with:\n%s"
                        % (target_bytes, new_target_bytes)
                    )
                fh.seek(0)
                fh.write(new_content)
        logging.debug(
            "patching took us {:.2f} seconds".format(time.perf_counter() - start)
        )

if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
        datefmt='%Y/%d/%m %H:%M:%S',
        level=logging.DEBUG,
        handlers=[logging.StreamHandler()]
    )
    patch_exe()
