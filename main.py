import os

# @profile
def get_last_line(file):
  CHUNK_SIZE = 200 # Would be good to make this the chunk size of the filesystem

  last_line = ""

  while True:
    # We grab chunks from the end of the file towards the beginning until we 
    # get a new line
    file.seek(-len(last_line) - CHUNK_SIZE, os.SEEK_END)
    chunk = file.read(CHUNK_SIZE)
    # print(chunk)

    if not chunk:
      # The whole file is one big line
      return last_line

    if not last_line and chunk.endswith(b'\n'):
      # Ignore the trailing newline at the end of the file (but include it 
      # in the output).
      last_line = b'\n'
      chunk = chunk[:-1]

    nl_pos = chunk.rfind(b'\n')
    # What's being searched for will have to be modified if you are searching
    # files with non-unix line endings.

    last_line = chunk[nl_pos + 1:] + last_line

    if nl_pos == -1:
      # The whole chunk is part of the last line.
      continue

    last_line = last_line.decode().strip()
    return last_line


# @profile
def get_nlast_line(file, n=500):
    CHUNK_SIZE = 128*n

    last_line = b""
    line_count = 0

    while True:
        file.seek(-len(last_line) - CHUNK_SIZE, os.SEEK_END)
        chunk = file.read(CHUNK_SIZE)

        if not chunk:
            return last_line


        while True:
            nl_pos = chunk.rfind(b'\n')

            last_line = chunk[nl_pos:] + last_line
            chunk = chunk[:nl_pos]

            if nl_pos == -1 or line_count == n + 1:
                break
            else:
                line_count += 1

        if line_count != n + 1:
            continue

        last_line = last_line.split(b'\n')
        last_line = list(filter(None, last_line))[-n:]
        last_line = list(map(lambda x: x.decode(), last_line))
        print(f'Total Lines :{len(last_line)}')

        return last_line


if __name__ == '__main__':
    with open('file.txt', 'rb') as f:
        # l = [i for i in range(10)]
        # for i in l:
        #     print(get_nlast_line(f, i))
        print(get_last_line(f))