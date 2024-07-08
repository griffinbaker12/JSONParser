#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef enum {
  TOKEN_STRING,
  TOKEN_NUMBER,
  TOKEN_TRUE,
  TOKEN_FALSE,
  TOKEN_NULL,
  TOKEN_LEFT_BRACE,
  TOKEN_RIGHT_BRACE,
  TOKEN_LEFT_BRACKET,
  TOKEN_RIGHT_BRACKET,
  TOKEN_COMMA,
  TOKEN_COLON,
  TOKEN_END
} TokenType;

typedef struct {
  TokenType type;
  char *value; // Now a pointer for dynamic allocation
} Token;

typedef struct {
  Token *tokens; // Now a pointer for dynamic allocation
  int count;
  int capacity;
} TokenArray;

TokenArray *create_token_array() {
  TokenArray *array = malloc(sizeof(TokenArray));
  array->capacity = 10; // Start with a small capacity
  array->tokens = malloc(array->capacity * sizeof(Token));
  array->count = 0;
  return array;
}

void add_token(TokenArray *array, TokenType type, const char *value) {
  if (array->count == array->capacity) {
    array->capacity *= 2;
    array->tokens = realloc(array->tokens, array->capacity * sizeof(Token));
  }
  array->tokens[array->count].type = type;
  array->tokens[array->count].value =
      strdup(value); // Allocate and copy the string
  array->count++;
}

TokenArray *lexer(const char *input) {
  TokenArray *tokenArray = create_token_array();

  const char *p = input;
  while (*p != '\0') {
    // Skip whitespace
    while (isspace(*p))
      p++;

    if (*p == '{') {
      add_token(tokenArray, TOKEN_LEFT_BRACE, "{");
      p++;
    } else if (*p == '}') {
      add_token(tokenArray, TOKEN_RIGHT_BRACE, "}");
      p++;
    } else if (*p == '[') {
      add_token(tokenArray, TOKEN_LEFT_BRACKET, "[");
      p++;
    } else if (*p == ']') {
      add_token(tokenArray, TOKEN_RIGHT_BRACKET, "]");
      p++;
    } else if (*p == ',') {
      add_token(tokenArray, TOKEN_COMMA, ",");
      p++;
    } else if (*p == ':') {
      add_token(tokenArray, TOKEN_COLON, ":");
      p++;
    } else if (*p == '"') {
      // String
      const char *start = ++p;
      while (*p != '"' && *p != '\0')
        p++;
      if (*p == '"') {
        int length = p - start;
        char *value = malloc(length + 1);
        strncpy(value, start, length);
        value[length] = '\0';
        add_token(tokenArray, TOKEN_STRING, value);
        free(value);
        p++;
      }
    } else if (isdigit(*p) || *p == '-') {
      // Number
      const char *start = p;
      while (isdigit(*p) || *p == '.' || *p == 'e' || *p == 'E' || *p == '+' ||
             *p == '-')
        p++;
      int length = p - start;
      char *value = malloc(length + 1);
      strncpy(value, start, length);
      value[length] = '\0';
      add_token(tokenArray, TOKEN_NUMBER, value);
      free(value);
    } else if (strncmp(p, "true", 4) == 0) {
      add_token(tokenArray, TOKEN_TRUE, "true");
      p += 4;
    } else if (strncmp(p, "false", 5) == 0) {
      add_token(tokenArray, TOKEN_FALSE, "false");
      p += 5;
    } else if (strncmp(p, "null", 4) == 0) {
      add_token(tokenArray, TOKEN_NULL, "null");
      p += 4;
    } else {
      // Unrecognized character, skip it
      p++;
    }
  }

  add_token(tokenArray, TOKEN_END, "");
  return tokenArray;
}

void print_tokens(TokenArray *tokenArray) {
  const char *token_names[] = {
      "STRING",
      "NUMBER",
      "TRUE",
  };

  for (int i = 0; i < tokenArray->count; i++) {
    printf("Token %d: Type = %s, Value = '%s'\n", i,
           token_names[tokenArray->tokens[i].type],
           tokenArray->tokens[i].value);
  }
}

void free_token_array(TokenArray *tokenArray) {
  for (int i = 0; i < tokenArray->count; i++) {
    free(tokenArray->tokens[i].value);
  }
  free(tokenArray->tokens);
  free(tokenArray);
}

// Test the lexer
int main() {
  const char *json_string = "{\n"
                            "  \"name\": \"John Doe\",\n"
                            "  \"age\": 30,\n"
                            "  \"is_student\": false,\n"
                            "  \"grades\": [85, 90, 78.5],\n"
                            "  \"address\": null\n"
                            "}";

  TokenArray *tokens = lexer(json_string);
  print_tokens(tokens);
  free_token_array(tokens);

  return 0;
}
