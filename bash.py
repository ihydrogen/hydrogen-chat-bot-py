from subprocess import Popen, PIPE


def bash(cmd):
    p = Popen(['bash', '-c', cmd], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    return str(output.decode('ascii')).replace("\n", "")
