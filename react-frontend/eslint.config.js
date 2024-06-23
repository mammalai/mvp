import { fixupConfigRules, fixupPluginRules } from '@eslint/compat';
import prettier from 'eslint-plugin-prettier';
import react from 'eslint-plugin-react';
import reactHooks from 'eslint-plugin-react-hooks';
import globals from 'globals';
import babelParser from '@babel/eslint-parser';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import js from '@eslint/js';
import { FlatCompat } from '@eslint/eslintrc';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const compat = new FlatCompat({
  baseDirectory: __dirname,
  recommendedConfig: js.configs.recommended,
  allConfig: js.configs.all,
});

export default [
  ...fixupConfigRules(
    compat.extends(
      'prettier',
      'plugin:react/jsx-runtime',
      'plugin:jsx-a11y/recommended',
      'plugin:react-hooks/recommended',
      'eslint:recommended',
      'plugin:react/recommended',
    ),
  ),
  {
    plugins: {
      prettier,
      react: fixupPluginRules(react),
      'react-hooks': fixupPluginRules(reactHooks),
    },

    languageOptions: {
      globals: {
        ...globals.browser,
      },

      parser: babelParser,
      ecmaVersion: 12,
      sourceType: 'script',

      parserOptions: {
        sourceType: 'module',
        ecmaFeatures: {
          experimentalObjectRestSpread: true,
          impliedStrict: true,
          jsx: true,
        },
      },
    },

    settings: {
      react: {
        createClass: 'createReactClass',
        pragma: 'React',
        fragment: 'Fragment',
        version: 'detect',
        flowVersion: '0.53',
      },

      'import/resolver': {
        node: {
          moduleDirectory: ['node_modules', 'src/'],
        },
      },
    },

    rules: {
      'react/jsx-uses-react': 'error',
      'react/jsx-uses-vars': 'error',
      'react/react-in-jsx-scope': 'off',
      'no-undef': 'off',
      'react/display-name': 'off',
      'react/jsx-filename-extension': 'off',
      'no-param-reassign': 'off',
      'react/prop-types': 1,
      'react/require-default-props': 'off',
      'react/no-array-index-key': 'off',
      'react/jsx-props-no-spreading': 'off',
      'react/forbid-prop-types': 'off',
      'import/order': 'off',
      'import/no-cycle': 'off',
      'no-console': 'off',
      'jsx-a11y/anchor-is-valid': 'off',
      'prefer-destructuring': 'off',
      'no-shadow': 'off',
      'import/no-named-as-default': 'off',
      'import/no-extraneous-dependencies': 'off',
      'jsx-a11y/no-autofocus': 'off',

      'no-restricted-imports': [
        'error',
        {
          patterns: ['@mui/*/*/*', '!@mui/material/test-utils/*'],
        },
      ],

      'no-unused-vars': [
        'error',
        {
          ignoreRestSiblings: false,
        },
      ],

      'prettier/prettier': [
        'error',
        {
          bracketSpacing: true,
          singleQuote: true,
          trailingComma: 'all',
          tabWidth: 2,
          useTabs: false
        },
      ],
    },
  },
];
