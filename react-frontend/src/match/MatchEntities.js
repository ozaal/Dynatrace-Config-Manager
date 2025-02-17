import { Paper, Typography } from '@mui/material';
import * as React from 'react';
import { MATCH_ENTITIES_V2 } from '../backend/backend';
import { useTreeResult } from './AnalysisResultHook';
import MatchButton from './MatchButton';
import MatchTypeLegend from './MatchTypeLegend';

export default function MatchEntities() {

    const { setAnalysisResult, analysisResultComponent } = useTreeResult(undefined, undefined)

    return (
        <Paper elevation={0}>
            <MatchButton handleChange={setAnalysisResult} api={MATCH_ENTITIES_V2} label="Match Entities V2" />
            <Paper elevation={0} sx={{ mt: 1 }}>
                {analysisResultComponent}
            </Paper>
            <Typography sx={{ mt: 2 }}>Legend:</Typography>
            <MatchTypeLegend />
        </Paper>
    );
}
