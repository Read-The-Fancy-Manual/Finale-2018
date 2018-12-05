/*
    Compilation:

    gcc -Wall -Wextra -Werror -Wl,-z,relro -fstack-protector -fpie chall.c -o chall

    Compiled with gcc version 8.2.0 (Debian 8.2.0-4)
*/

#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <stdint.h>
#include <stdlib.h>

#define MAX_MESSAGES 0x10


typedef struct message_s
{
    uint64_t pad;
    char * displayedMessage;
    uint64_t messageLen;
    uint64_t panelID;
} message_t;

uint64_t nbMessages = 0;
message_t * messages[MAX_MESSAGES];

void my_puts(const char * string)
{
    puts(string);
    fflush(stdout);
}

char * getString(char *dst, uint64_t len, FILE * stream)
{
    char * ret;

    ret = fgets(dst, len, stream);

    if (!ret)
    {
        perror("[-] fgets failed");
        exit(1);
    }
    ret = strchr(ret, 10);
    if (ret)
        *ret = 0;
    return ret;
}

uint64_t getNumber()
{
    char number[65];

    getString(number, 64, stdin);
    return strtol(number, 0LL, 10);
}

void malloc_failed()
{
    my_puts("[-] Malloc failed !");
    exit(1);
}

void prompt()
{
    write(1, ">> ", 3);
}

message_t * findMessage(uint64_t panelID)
{
    uint64_t i = 0;
    uint64_t j = 0;

    if (!nbMessages)
        return NULL;

    while (j < nbMessages && i < MAX_MESSAGES)
    {
        if (messages[i])
        {
            j++;
            if (messages[i]->panelID == panelID)
                return messages[i];
        }
        i++;
    }
    return NULL;
}

void createPanelMessage(uint64_t panelID)
{
    uint64_t messageLen;
    char * message;
    message_t * msg_struct;
    uint64_t i = 0;

    if (nbMessages + 1 > MAX_MESSAGES)
    {
        my_puts("[-] Already too much messages !");
        return;
    }

    printf("[+] Creating a new message on panel number [%lu]\n", panelID);
    my_puts("[?] Length of your message (1-1023):");
    prompt();

    messageLen = getNumber();

    if (!messageLen || messageLen > 1023)
    {
        my_puts("[!] Length invalid !");
        return;
    }


    msg_struct = malloc(sizeof(message_t));
    message = malloc(messageLen);
    if (!msg_struct || !message)
        malloc_failed();

    my_puts("[?] Content of your message:");
    prompt();
    getString(message, messageLen, stdin);
    
    msg_struct->panelID = panelID;
    msg_struct->messageLen = messageLen;
    msg_struct->displayedMessage = message;

    for (i = 0; messages[i]; i++)
    {
        if (i >= MAX_MESSAGES)
        {
            my_puts("[-] Fatal error: No empty space for the message !");
            exit(1);
        }
    }
    
    messages[i] = msg_struct;
    nbMessages++;
    return;
}


void editPanelMessage(uint64_t panelID)
{
    message_t * msg;

    msg = findMessage(panelID);
    if (!msg)
    {
        my_puts("[-] No message on this panel !");
        return;
    }

    printf("[+] Editing message on panel number [%lu]\n", panelID);

    my_puts("[?] New content of your message:");
    prompt();
    getString(msg->displayedMessage, msg->messageLen, stdin);
}

void deletePanelMessage(uint64_t panelID)
{
    message_t * msg;
    uint64_t i = 0;

    msg = findMessage(panelID);
    if (!msg)
    {
        my_puts("[-] No message on this panel !");
        return;
    }

    printf("[+] Deleting message on panel number [%lu]\n", panelID);

    free(msg->displayedMessage);
    free(msg);

    for (i = 0; i <= nbMessages; i++)
    {
        if (messages[i] == msg)
        {
            messages[i] = NULL;
            break;
        }
    }
    nbMessages--;
}

void menu()
{
    uint64_t i = 0;
    uint64_t panelID;

    while (1)
    {

        my_puts("1. Print a message on a panel");
        my_puts("2. Edit a message on a panel");
        my_puts("3. Clear a panel");
        my_puts("4. List panels");
        my_puts("5. Quit");
        prompt();
        switch (getNumber())
        {
            case 1:
                my_puts("[?] Panel ID to display message on (0-15):");
                prompt();
                panelID = getNumber();
                if (panelID > MAX_MESSAGES)
                {
                    my_puts("[-] No panel found with this ID");
                    continue;
                }
                if (findMessage(panelID) != NULL)
                {
                    my_puts("[-] There is already a message on this panel");
                    continue;
                }
                createPanelMessage(panelID);
                continue;

            case 2:
                my_puts("[?] Panel ID to edit message on (0-15):");
                prompt();
                panelID = getNumber();
                if (panelID > MAX_MESSAGES)
                {
                    my_puts("[-] No panel found with this ID");
                    continue;
                }
                editPanelMessage(panelID);
                continue;

            case 3:
                my_puts("[?] Panel ID to clear message on (0-15):");
                prompt();
                panelID = getNumber();
                if (panelID > MAX_MESSAGES)
                {
                    my_puts("[-] No panel found with this ID");
                    continue;
                }
                deletePanelMessage(panelID);
                continue;
            case 4:
                printf("[+] You currently have %lu messages\n", nbMessages);
                for (i = 0; i <= MAX_MESSAGES; i++)
                {
                    if (messages[i])
                        printf("[+] [%02lu][%s]\n", messages[i]->panelID, messages[i]->displayedMessage);
                } 
                continue;
            case 5:
                return;
            default: 
                my_puts("[-] Invalid choice !");
                continue;
        }
    }
}

int main(void)
{
    uint64_t i = 0;

    nbMessages = 0;
    for (i = 0; i < MAX_MESSAGES; i++)
    {
        messages[i] = NULL;
    } 

    my_puts("Welcome in DisplayPanelManager ! Please chose something to do:");
    menu();
    my_puts("Bye !");
}
