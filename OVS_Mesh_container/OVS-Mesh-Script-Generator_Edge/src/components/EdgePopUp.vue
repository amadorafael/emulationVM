<!-- New File to Link PopUp -->

<template>
    <div id="edge-popUp" class="modal fade" tabindex="-1" role="dialog">
        <div class="modal-dialog modal-sm" role="document">
            <div class="modal-content">
                <div class="modal-header my-blue-bg">
                    <button type="button" id="close-btn-top" class="close my-white-font" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
                    <h4 class="modal-title my-white-font" id="operation"></h4>
                </div>
                <div class="modal-body">
                    <div class="form-group">
                        <label for="edge-value">Link Speed (Mbps):</label>
                        <select class="form-control" id="edge-value">
                            <option value="100" selected>100 Mbps</option>
                            <option value="50">50 Mbps</option>
                        </select>
                    </div>
                </div>
                <div class="modal-footer">
                    <button id="cancel-button" type="button" data-dismiss="modal" class="btn btn-default">
                        Cancel
                    </button>

                    <button type="button" id="edgeSaveButton" class="btn btn-primary my-blue-button">
                        <i class="fa fa-fw fa-check"></i>
                        <span id="saveButton-text"></span>
                    </button>
                </div>
            </div>

          </div>
    </div>
</template>


